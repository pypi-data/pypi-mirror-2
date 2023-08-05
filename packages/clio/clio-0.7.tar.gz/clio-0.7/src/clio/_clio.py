from datetime import datetime

from sqlalchemy.orm import (object_mapper, class_mapper, object_session,
                            RelationProperty)
from sqlalchemy.orm.interfaces import ONETOMANY, MANYTOONE, MANYTOMANY
from sqlalchemy.sql import select, insert
from sqlalchemy.orm.properties import BackRef
from sqlalchemy import and_, or_
from sqlalchemy import func
from sqlalchemy import Table as SATable
from sqlalchemy import Column, Integer, Unicode, DateTime, UniqueConstraint

from zope.interface import implements
from zope import component
from clio.interfaces import IClioModel, ICurrentUserId

NEW = 0
EDITABLE = 1
UPDATABLE = 2
DELETED = 3
DELETED_EDITABLE = 4
DELETED_UPDATABLE = 5
PUBLISHED = 6
PUBLISHED_UNDER_EDIT = 7
PUBLISHED_UNDER_UPDATE = 8
PUBLISHED_UNDER_DELETE = 9
ARCHIVED = 1000

PUBLISHED_STATUSES = (PUBLISHED, PUBLISHED_UNDER_EDIT, PUBLISHED_UNDER_UPDATE,
                      PUBLISHED_UNDER_DELETE)
DELETED_STATUSES = (DELETED, DELETED_EDITABLE, DELETED_UPDATABLE)
NEW_VERSION_STATUSES = (NEW, EDITABLE, UPDATABLE) + DELETED_STATUSES

# any statuses applicable to an edit UI
EDITABLE_STATUSES = NEW_VERSION_STATUSES + (PUBLISHED,)
# any statuses that count as as actual (not-deleted) in the edit UI
ACTUAL_STATUSES = (NEW, EDITABLE, UPDATABLE, PUBLISHED)

class ClioError(Exception):
    pass

class PublishError(ClioError):
    pass

class EditError(ClioError):
    pass

class UpdateError(ClioError):
    pass

class DeleteError(ClioError):
    pass

class CompareError(ClioError):
    pass

class RevertError(ClioError):
    pass

def Table(name, metadata, *args, **kw):
    """Like SQLAlchemy's Table but adding the standard clio fields.
    """
    return SATable(name, metadata,
                   Column('id', Integer, primary_key=True),
                   Column('code', Integer, nullable=False, index=True),
                   Column('status', Integer, nullable=False, index=True),
                   Column('created_timestamp', DateTime, nullable=False),
                   Column('published_start_timestamp', DateTime, nullable=True,
                          index=True),
                   Column('published_end_timestamp', DateTime, nullable=True,
                          index=True),
                   Column('changed_timestamp', DateTime, nullable=True),
                   Column('created_userid', Unicode(64), nullable=True,
                          index=True),
                   Column('published_userid', Unicode(64), nullable=True,
                          index=True),
                   Column('changed_userid', Unicode(64), nullable=True,
                          index=True),
                   UniqueConstraint('code', 'status', name='workflow'),
                   *args, **kw)

class WrapProperty(object):
    def __init__(self, key):
        self.key = key

    def __get__(self, instance, owner):
        if instance.status == UPDATABLE:
            return getattr(instance._version(PUBLISHED_UNDER_UPDATE),
                           self.key + '_original')
        return getattr(instance, self.key + '_original')

    # the presence of this method magically makes sure that this property
    # doesn't get overwritten to become a boolean...
    def __set__(self, instance, owner, value):
        pass
        
class WorkflowProperty(object):
    def __init__(self, target_table, key):
        self.key = key
        self.target_table = target_table
        
    def __get__(self, instance, owner):
        q = getattr(instance, self.key)
        return self.filter(q)

    def filter(self, query):
        raise NotImplementedError

class StatusProperty(WorkflowProperty):
    def __init__(self, target_table, key, states):
        super(StatusProperty, self).__init__(target_table, key)
        self.states = states
        
    def filter(self, query):
        return query.filter(self.target_table.c.status.in_(self.states))

class ArchivedProperty(WorkflowProperty):
    def filter(self, query):
        return query.filter(self.target_table.c.status >= ARCHIVED)
    
def workflow_properties(class_):
    m = class_mapper(class_)
    for prop in m.iterate_properties:
        if isinstance(prop, RelationProperty):
            if prop.direction in (ONETOMANY, MANYTOMANY):
                setattr(class_, prop.key + '_original',
                        getattr(class_, prop.key))
                setattr(class_, prop.key, WrapProperty(prop.key))
                setattr(class_, prop.key + '_archived',
                        ArchivedProperty(prop.target, prop.key))
                setattr(class_, prop.key + '_published',
                        StatusProperty(prop.target, prop.key,
                                       PUBLISHED_STATUSES))
                setattr(class_, prop.key + '_editable',
                        StatusProperty(prop.target, prop.key,
                                       EDITABLE_STATUSES))
                setattr(class_, prop.key + '_actual',
                        StatusProperty(prop.target, prop.key,
                                       ACTUAL_STATUSES))

class ComparisonResult(object):
    def __init__(self, edited, deleted, unchanged):
        self.edited = edited
        self.deleted = deleted
        self.unchanged = unchanged

class Model(object):
    """Base class of all workflowed models.
    """
    implements(IClioModel)
    
    def __init__(self, code):
        self.code = code
        self.status = NEW
        self.created_timestamp = self._now()
        self.created_userid = self._get_userid()

        # when you create a new object from scratch, you've
        # also changed it
        self.changed_timestamp = self.created_timestamp
        self.changed_userid = self.created_userid

        self.published_start_timestamp = None
        self.published_end_timestamp = None
        self.published_userid = None
        
    def publish(self):
        if self.is_archived():
            raise PublishError("Cannot publish an archived object.")
        elif self.status == PUBLISHED:
            return self        
        elif self.status == PUBLISHED_UNDER_EDIT:
            return self._version(EDITABLE).publish()        
        elif self.status == PUBLISHED_UNDER_UPDATE:
            return self._version(UPDATABLE).publish()
        elif self.status == PUBLISHED_UNDER_DELETE:
            return self._deleted_version().publish()
        
        if self.status == NEW:
            if self._has_unpublished_parent():
                raise PublishError(
                    "Cannot publish object that has "
                    "an unpublished parent object.")
            self.status = PUBLISHED
            self.published_start_timestamp = self._now()
            self.published_userid = self._get_userid()
            self._publish_related()
            return self
        elif self.status == EDITABLE:
            published = self._version(PUBLISHED_UNDER_EDIT)
            timestamp = self._now()
            published._archive(timestamp)
            self.status = PUBLISHED
            self.published_start_timestamp = timestamp
            self.published_userid = self._get_userid()
            self._publish_related()
            return self
        elif self.status == UPDATABLE:
            # first we copy over the relations from the published
            # version over to this version
            published = self._version(PUBLISHED_UNDER_UPDATE)
            self._move_relations(published)
            timestamp = self._now()
            published._archive(timestamp)
            self.status = PUBLISHED
            self.published_start_timestamp = timestamp
            self.published_userid = self._get_userid()
            return self
        elif self.status in DELETED_STATUSES:
            published = self._version(PUBLISHED_UNDER_DELETE)
            published.published_userid = self._get_userid()
            published._archive(self._now())
            self._publish_related()
            session = object_session(self)
            session.delete(self)
            return published
        else:
            raise PublishError(
                "Cannot publish object of unknown status: %s" % self.status)

    def edit(self):
        if self.is_archived():
            raise EditError("Cannot edit an archived object.")
        elif self.status in (UPDATABLE, PUBLISHED_UNDER_UPDATE):
            raise EditError("Cannot edit an updatable object.")
        elif self.status in (EDITABLE, NEW):
            return self        
        elif self.status == PUBLISHED_UNDER_EDIT:
            return self._version(EDITABLE)
        elif self.status == PUBLISHED_UNDER_DELETE:
            return self._deleted_version().edit()

        if self.status in DELETED_STATUSES:
            return self.revert().edit()
            
        if self.status != PUBLISHED:
            raise EditError(
                "Cannot edit object of unknown status: %s" % self.status)
        result = self._create_edit_copy() 
        self.status = PUBLISHED_UNDER_EDIT
        session = object_session(self)
        session.add(result)
        return result

    def update(self):
        if self.is_archived():
            raise UpdateError("Cannot update an archived object.")
        elif self.status in (EDITABLE, PUBLISHED_UNDER_EDIT):
            raise UpdateError("Cannot update an editable object.")
        elif self.status in (UPDATABLE, NEW):
            return self
        elif self.status == PUBLISHED_UNDER_UPDATE:
            return self._version(UPDATABLE)
        elif self.status == PUBLISHED_UNDER_DELETE:
            return self._deleted_version().update()

        if self.status in DELETED_STATUSES:
            return self.revert().update()
        
        if self.status != PUBLISHED:
            raise UpdateError(
                "Cannot update object of unknown status: %s" % self.status)
        result = self._create_update_copy()
        self.status = PUBLISHED_UNDER_UPDATE
        session = object_session(self)
        session.add(result)
        return result

    def delete(self):
        if self.is_archived():
            raise DeleteError("Cannot delete an archived object.")
        elif self.status in DELETED_STATUSES:
            return self
        elif self.status == PUBLISHED_UNDER_DELETE:
            return self._deleted_version()
        
        if self.status == NEW:
            session = object_session(self)
            session.delete(self)
            return None
        elif self.status == UPDATABLE:
            self._delete_related()
            self.status = DELETED_UPDATABLE
            published = self._version(PUBLISHED_UNDER_UPDATE)
            published.status = PUBLISHED_UNDER_DELETE
            return self
        elif self.status == EDITABLE:
            self._delete_related()
            self.status = DELETED_EDITABLE
            published = self._version(PUBLISHED_UNDER_EDIT)
            published.status = PUBLISHED_UNDER_DELETE
            return self
        elif self.status == PUBLISHED:            
            result = self._create_delete_copy()
            session = object_session(self)
            session.add(result)
            self.status = PUBLISHED_UNDER_DELETE
            result.status = DELETED
            result._delete_related()
            return result
        else:            
            raise DeleteError(
                "Cannot delete object of unknown status: %s" % self.status)

    def revert(self):
        if self.is_archived():
            return self # raise RevertError("Cannot revert an archived object.")
        elif self.status == PUBLISHED_UNDER_EDIT:
            return self._version(EDITABLE).revert()
        elif self.status == PUBLISHED_UNDER_UPDATE:
            return self._version(UPDATABLE).revert()
        elif self.status == PUBLISHED_UNDER_DELETE:
            return self._deleted_version().revert()
        
        if self.status == NEW:
            session = object_session(self)
            session.delete(self)
            return None
        elif self.status == EDITABLE:
            published = self._version(PUBLISHED_UNDER_EDIT)
            published._create_edit_copy_onto(self)
            self._revert_related()
            return self
        elif self.status == UPDATABLE:
            published = self._version(PUBLISHED_UNDER_UPDATE)
            published._create_update_copy_onto(self)
            self._revert_related()
            return self
        elif self.status == DELETED:
            published = self._version(PUBLISHED_UNDER_DELETE)
            session = object_session(self)
            published.status = PUBLISHED
            published._revert_related()
            session.delete(self)
            return published
        elif self.status == DELETED_EDITABLE:
            published = self._version(PUBLISHED_UNDER_DELETE)
            self.status = EDITABLE
            self._revert_related()
            published.status = PUBLISHED_UNDER_EDIT
            return self
        elif self.status == DELETED_UPDATABLE:
            published = self._version(PUBLISHED_UNDER_DELETE)
            self.status = UPDATABLE
            self._revert_related()
            published.status = PUBLISHED_UNDER_UPDATE
            return self
        elif self.status == PUBLISHED:
            self._revert_related()
            return self
        else:
            raise RevertError(
                "Cannot revert object of unknown status: %s" % self.status)

    def is_editable(self):
        return self.status in NEW_VERSION_STATUSES

    def is_actual(self):
        return self.status in ACTUAL_STATUSES

    def is_published(self):
        return self.status in PUBLISHED_STATUSES
    
    def is_archived(self):
        return self.status >= ARCHIVED

    def is_deleted(self):
        return self.status in DELETED_STATUSES

    def editable_version(self):
        """Give version that's visible in to an edit UI, if any.

        If only archived versions exist, None is returned.
        """
        q = self._versions_query()
        return q.filter(self.__class__.status.in_(EDITABLE_STATUSES)).first()

    def compare_relation(self, relation_name):
        if self.status == EDITABLE:
            editable = self
            published = self._version(PUBLISHED_UNDER_EDIT)
        elif self.status == PUBLISHED_UNDER_EDIT:
            editable = self._version(EDITABLE)
            published = self
        elif self.status == PUBLISHED:
            editable = None
            published = self
        if editable is not None:
            relation = getattr(editable, relation_name)
        else:
            relation = getattr(published, relation_name)
        editable = []
        deleted = []
        unchanged = []
        for obj in relation:
            if obj.status == EDITABLE:
                editable.append(obj)
            elif obj.status == PUBLISHED:
                unchanged.append(obj)
            elif obj.status in DELETED_STATUSES:
                deleted.append(obj)
        return ComparisonResult(editable, deleted, unchanged)        

    def mark_changed(self):
        self.changed_timestamp = self._now()
        self.changed_userid = self._get_userid()
            
    # PRIVATE
    def _now(self):
        return datetime.now()
    
    def _get_userid(self):
        try:
            return component.getUtility(ICurrentUserId)()
        except component.ComponentLookupError:
            return u'unknown'

    def _archive(self, timestamp):
        self.status = self._get_next_archive_status()
        self.published_end_timestamp = timestamp
        return self

    def _get_relation_props(self, *directions):
        m = object_mapper(self)
        for prop in m.iterate_properties:
            if isinstance(prop, RelationProperty):
                if prop.direction in directions:
                    yield prop

    def _get_other_props(self):
        m = object_mapper(self)
        for prop in m.iterate_properties:
            if not isinstance(prop, RelationProperty):
                yield prop
        
    def _get_related(self):
        for prop in self._get_relation_props(ONETOMANY):
            for related in getattr(self, prop.key + '_original'):
                yield related

    def _publish_related(self):
        for related in self._get_related():
            if related.status in NEW_VERSION_STATUSES:
                related.publish()

    def _delete_related(self):
        for related in self._get_related():
            if related.status in NEW_VERSION_STATUSES:
                related.delete()

    def _revert_related(self):
        for related in self._get_related():
            related.revert()

    def _has_unpublished_parent(self):
        for prop in self._get_relation_props(MANYTOONE):
            parent = getattr(self, prop.key)
            if parent.status not in PUBLISHED_STATUSES:
                return True
        return False

    def _get_next_archive_status(self):
        session = object_session(self)
        status = session.query(func.max(self.__class__.status)).first()[0]
        if status < ARCHIVED:
            status = ARCHIVED
        else:
            status += 1        
        return status

    def _create_update_copy(self):
        m = object_mapper(self)
        mgr = m.class_manager
        result = mgr.new_instance()
        for prop in self._get_other_props():
            value = getattr(self, prop.key)
            setattr(result, prop.key, value)
        # the copy is not published
        result.published_start_timestamp = None
        result.published_end_timestamp = None
        result.published_userid = None
        # the copy has just been created
        result.created_timestamp = result._now()
        result.created_userid = self._get_userid()
        del result.id
        result.status = UPDATABLE
        return result

    def _create_update_copy_onto(self, target):
        result = target
        dont_overwrite = set(['id'])
        for prop in self._get_relation_props(MANYTOONE):
            for entry in prop.local_side:
                dont_overwrite.add(entry.name)
        for prop in self._get_other_props():
            if prop.key not in dont_overwrite:
                value = getattr(self, prop.key)
                setattr(result, prop.key, value)
        result.status = UPDATABLE
        # the copy is not published
        result.published_start_timestamp = None
        result.published_end_timestamp = None
        result.published_userid = None
        # the copy has just been created
        result.created_timestamp = result._now()
        result.created_userid = self._get_userid()
        return result

    def _create_edit_copy(self):
        result = self._create_update_copy()
        result.status = EDITABLE

        # this has to be done *after* the basic properties of result
        # are set otherwise relations don't get set up properly
        for prop in self._get_relation_props(ONETOMANY, MANYTOMANY):
            if prop.direction == ONETOMANY:
                orig_values = getattr(self, prop.key)
                values = getattr(result, prop.key)
                for related in orig_values[:]:
                    if related.status in NEW_VERSION_STATUSES:
                        orig_values.remove(related)
                        values.append(related)
                    elif related.status == PUBLISHED:
                        values.append(related._create_edit_copy())
                        related.status = PUBLISHED_UNDER_EDIT
            elif prop.direction == MANYTOMANY:
                orig_values = getattr(self, prop.key)
                values = getattr(result, prop.key)
                for related in orig_values[:]:
                    if related.status == PUBLISHED:
                        values.append(related)
        return result

    def _create_delete_copy(self):
        result = self._create_update_copy()
        result.status = DELETED
        # this has to be done *after* the basic properties of result
        # are set otherwise relations don't get set up properly
        for prop in self._get_relation_props(ONETOMANY, MANYTOMANY):
            if prop.direction is ONETOMANY:
                orig_values = getattr(self, prop.key)
                values = getattr(result, prop.key)
                for related in orig_values[:]:
                    if related.status in NEW_VERSION_STATUSES:
                        orig_values.remove(related)
                        values.append(related)
                        related.status = DELETED
                    elif related.status == PUBLISHED:
                        values.append(related._create_delete_copy())
                        related.status = PUBLISHED_UNDER_DELETE
            elif prop.direction is MANYTOMANY:
                orig_values = getattr(self, prop.key)
                values = getattr(result, prop.key)
                for related in orig_values[:]:
                    if related.status == PUBLISHED:
                        values.append(related)
        return result

    def _create_edit_copy_onto(self, target):
        result = self._create_update_copy_onto(target)
        result.status = EDITABLE
        # this has to be done *after* the basic properties of result
        # are set otherwise relations don't get set up properly
#         for prop in self._get_relation_props(ONETOMANY):
#             orig_values = getattr(self, prop.key)
#             values = getattr(result, prop.key)
#             for related in orig_values[:]:
#                 if related.status == PUBLISHED:
#                     values.append(related._create_edit_copy())
#                     related.status = PUBLISHED_UNDER_EDIT
        return result
        
    def _move_relations(self, source):
        for prop in self._get_relation_props(ONETOMANY):
            orig_values = getattr(source, prop.key + '_original')
            values = getattr(self, prop.key + '_original')
            for related in orig_values[:]:
                orig_values.remove(related)
                values.append(related)

    def _versions_query(self):
        session = object_session(self)
        return session.query(self.__class__).filter(
            self.__class__.code == self.code)
        
    def _version(self, status):
        return self._versions_query().filter(
            self.__class__.status == status).first()

    def _has_older_archived_version(self):
        q = self._versions_query()
        if self.is_published():
            return q.filter(
                self.__class__.status >= ARCHIVED).first() is not None
        else:
            return q.filter(
                and_(self.__class__.status >= ARCHIVED,
                     self.__class__.status < self.status)).first() is not None
        
    def _is_last_version(self):
        q = self._versions_query()
        # if there is a newer archived version, this isn't the last version
        if q.filter(
            and_(self.__class__.status >= ARCHIVED,
                 self.__class__.status > self.status)).first() is not None:
            return False
        # if there is a non-archived version, this isn't the last version
        return q.filter(and_(self.__class__.status < ARCHIVED)).first() is None
        
    def _deleted_version(self):
        for status in DELETED_STATUSES:
            version = self._version(status)
            if version is not None:
                return version
        return None


HISTORY_CREATE = u'create'
HISTORY_PUBLISH = u'publish'
HISTORY_EDIT = u'edit'
HISTORY_CHANGE = u'change'
HISTORY_DELETE = u'delete'
HISTORY_EDIT_DELETE = u'edit_delete'
HISTORY_ARCHIVE = u'archive'

class HistoryEvent(object):
    def __init__(self, event_type, timestamp, version, userid):
        """Construct a HistoryEvent.

        event_type: a historical event (HISTORY_CREATE, etc).
        timestamp: the timestamp of the historical event.
        version: the version that was involved in this event.
        userid: the userid who initiated the event. Can be None
                if this cannot be reconstructed.
        """
        self.event_type = event_type
        self.timestamp = timestamp
        self.version = version
        self.userid = userid


def _history_key(event):
    # archiving should always take place before publishing if the time is
    # the same, guarantee consistent sorting order
    # similarly, editing should always take place before change if time
    # is the same
    if event.event_type == HISTORY_PUBLISH:
        extra_sort = 1
    elif event.event_type == HISTORY_ARCHIVE:
        extra_sort = 0
    elif event.event_type == HISTORY_CHANGE:
        extra_sort = 1
    elif event.event_type == HISTORY_EDIT:
        extra_sort = 0
    else:
        extra_sort = 0
    # microseconds aren't recorded by the database
    timestamp = event.timestamp.replace(microsecond=0)
    return timestamp, extra_sort

def _add_changed_event(result, version):
    # in updated databases it is possible for changed_timestamp to
    # be None
    if version.changed_timestamp is None:
        return
    if version.changed_timestamp > version.created_timestamp:
        result.append(HistoryEvent(HISTORY_CHANGE,
                                   version.changed_timestamp,
                                   version,
                                   version.changed_userid))
    
def history(versions):
    """Return historical information about ORM-mapped objects.

    Historical information consists of a list of historical events.
    This includes the creation of objects and their publication and
    archiving, and the version of the object involved. These events are 
    sorted in chronological order.

    The input to this function is an iterable of versions. These should
    include all historical versions of all objects that we want
    chronological information about. Usually such a list of versions
    can be obtained by using a relation or by doing a query.
    """
    result = []
    for version in versions:
        if version.status == NEW:
            result.append(HistoryEvent(HISTORY_CREATE,
                                       version.created_timestamp,
                                       version,
                                       version.created_userid))
            _add_changed_event(result, version)
        elif version.status == EDITABLE:
            result.append(HistoryEvent(HISTORY_EDIT,
                                       version.created_timestamp,
                                       version,
                                       version.created_userid))
            _add_changed_event(result, version)
        elif version.status == UPDATABLE:
            result.append(HistoryEvent(HISTORY_EDIT,
                                       version.created_timestamp,
                                       version,
                                       version.created_userid))
            _add_changed_event(result, version)
        elif version.status in DELETED_STATUSES:
            result.append(HistoryEvent(HISTORY_EDIT_DELETE,
                                       version.created_timestamp,
                                       version,
                                       version.created_userid))
            _add_changed_event(result, version)
        elif version.status in PUBLISHED_STATUSES:
            if version._has_older_archived_version():
                result.append(HistoryEvent(HISTORY_EDIT,
                                           version.created_timestamp,
                                           version,
                                           version.created_userid))
            else:
                result.append(HistoryEvent(HISTORY_CREATE,
                                           version.created_timestamp,
                                           version,
                                           version.created_userid))
            _add_changed_event(result, version)
            result.append(HistoryEvent(HISTORY_PUBLISH,
                                       version.published_start_timestamp,
                                       version,
                                       version.published_userid))
        elif version.status >= ARCHIVED:
            if version._has_older_archived_version():
                result.append(HistoryEvent(HISTORY_EDIT,
                                           version.created_timestamp,
                                           version,
                                           version.changed_userid))
            else:
                result.append(HistoryEvent(HISTORY_CREATE,
                                           version.created_timestamp,
                                           version,
                                           version.changed_userid))
            _add_changed_event(result, version)
            result.append(HistoryEvent(HISTORY_PUBLISH,
                                       version.published_start_timestamp,
                                       version,
                                       version.published_userid))
            if version._is_last_version():
                result.append(HistoryEvent(HISTORY_DELETE,
                                           version.published_end_timestamp,
                                           version,
                                           version.published_userid))
            else:
                result.append(HistoryEvent(HISTORY_ARCHIVE,
                                           version.published_end_timestamp,
                                           version,
                                           None))

    result.sort(key=_history_key)
    return result

