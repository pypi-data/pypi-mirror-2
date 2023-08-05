##############################################################################
#
# Copyright (c) 2002-2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: QueueCatalog.py 86692 2008-05-13 10:38:28Z andreasjung $
"""
# Python std. lib
import logging
import sets
import sys
from time import time
from types import StringType

# Other packages
from ZODB.POSException import ConflictError
from ZEO.Exceptions import ClientDisconnected
from zExceptions import Unauthorized
from ExtensionClass import Base
from OFS.SimpleItem import SimpleItem
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityInfo import ClassSecurityInformation
from AccessControl.Permissions \
     import manage_zcatalog_entries, view_management_screens
from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Globals import DTMLFile
from Acquisition import Implicit, aq_base, aq_inner, aq_parent

# Local
from CatalogEventQueue import CatalogEventQueue, EVENT_TYPES, ADDED_EVENTS
from CatalogEventQueue import ADDED, CHANGED, CHANGED_ADDED, REMOVED
from CatalogEventQueue import SAFE_POLICY, ALTERNATIVE_POLICY

logger = logging.getLogger('event.QueueCatalog')

_zcatalog_methods = {
    'catalog_object': 1,
    'uncatalog_object': 1,
    'uniqueValuesFor': 1,
    'getpath': 1,
    'getrid': 1,
    'getobject': 1,
    'schema': 1,
    'indexes': 1,
    'index_objects': 1,
    'searchResults': 1,
    '__call__': 1,
    'refreshCatalog': 1,
    'Indexes': 1,
    'unrestrictedSearchResults': 1,
    'manage_addIndex': 1,
    'manage_addColumn': 1,
    'manage_catalogClear': 1,
    'getIndexObjects': 1,
    }

_is_zcatalog_method = _zcatalog_methods.has_key

_views = {}


class QueueConfigurationError(Exception):
    pass


class QueueCatalog(Implicit, SimpleItem):
    """Queued ZCatalog (Proxy)

    A QueueCatalog delegates most requests to a ZCatalog that is named
    as part of the QueueCatalog configuration.

    Requests to catalog or uncatalog objects are queued. They must be
    processed by a separate process (or thread). The queuing provides
    benefits:

    - Content-management operations, performed by humans, complete
      much faster, this making the content-management system more
      effiecient for it's users.

    - Catalog updates are batched, which makes indexing much more
      efficient.

    - Indexing is performed by a single thread, allowing more
      effecient catalog document generation and avoiding conflict
      errors from occuring during indexing.

    - When used with ZEO, indexing might e performed on the same
      machine as the storage server, making updates faster.

    """

    security = ClassSecurityInformation()

    _immediate_indexes = ()  # The names of indexes to update immediately
    _location = None
    _immediate_removal = 1   # Flag: don't queue removal
    _immediate_metadata_update = 1 # Flag: don't queue metadata creation
    _process_all_indexes = 0 # Flag: queue-process all, not just non-immediate,
                             #       indexes
    title = ''


    # When set, _v_catalog_cache is a tuple containing the wrapped ZCatalog
    # and the REQUEST it is bound to.
    _v_catalog_cache = None

    # As an alternative to the original queue conflict handling there is now
    # a policy which will reduce conflicts, but at the cost of possibly having
    # situations where items get cataloged unnecessarily. YMMV.
    _conflict_policy = SAFE_POLICY

    def __init__(self, buckets=1009, conflict_policy=SAFE_POLICY):
        self._buckets = buckets
        self._conflict_policy = conflict_policy
        self._clearQueues()

    def _clearQueues(self):
        self._queues = [ CatalogEventQueue(self.getConflictPolicy()) 
                              for i in range(self._buckets) ]

    def getTitle(self):
        return self.title

    security.declareProtected(view_management_screens, 'setLocation')
    def setLocation(self, location):
        if self._location is not None:
            try:
                self.process()
            except QueueConfigurationError:
                self._clearQueues()
        self._location = location

    security.declareProtected(view_management_screens, 'getIndexInfo')
    def getIndexInfo(self):
        try:
            c = self.getZCatalog()
        except QueueConfigurationError:
            return None
        else:
            items = [(ob.id, ob.meta_type) for ob in c.getIndexObjects()]
            items.sort()
            res = []
            for id, meta_type in items:
                res.append({'id': id, 'meta_type': meta_type})
            return res


    security.declareProtected(view_management_screens, 'getImmediateIndexes')
    def getImmediateIndexes(self):
        return self._immediate_indexes

    security.declareProtected(view_management_screens, 'setImmediateIndexes')
    def setImmediateIndexes(self, indexes):
        self._immediate_indexes = tuple(map(str, indexes))

    security.declareProtected(view_management_screens, 'getImmediateRemoval')
    def getImmediateRemoval(self):
        return self._immediate_removal

    security.declareProtected(view_management_screens, 'setImmediateRemoval')
    def setImmediateRemoval(self, flag):
        self._immediate_removal = bool(flag)

    security.declareProtected(view_management_screens,
                              'getImmediateMetadataUpdate')
    def getImmediateMetadataUpdate(self):
        return self._immediate_metadata_update

    security.declareProtected(view_management_screens,
                              'setImmediateMetadataUpdate')
    def setImmediateMetadataUpdate(self, flag):
        self._immediate_metadata_update = bool(flag)

    security.declareProtected(view_management_screens, 'getProcessAllIndexes')
    def getProcessAllIndexes(self):
        return self._process_all_indexes

    security.declareProtected(view_management_screens, 'setProcessAllIndexes')
    def setProcessAllIndexes(self, flag):
        self._process_all_indexes = bool(flag)

    security.declareProtected(view_management_screens, 'getBucketCount')
    def getBucketCount(self):
        return self._buckets

    security.declareProtected(view_management_screens, 'setBucketCount')
    def setBucketCount(self, count):
        if self._location:
            self.process()
        self._buckets = int(count)
        self._clearQueues()

    security.declareProtected(view_management_screens, 'getConflictPolicy')
    def getConflictPolicy(self):
        """ Return the currently-used conflict policy
        """
        return self._conflict_policy

    security.declareProtected(view_management_screens, 'setConflictPolicy')
    def setConflictPolicy(self, policy=SAFE_POLICY):
        """ Set the conflic policy to be used
        """
        try:
            policy = int(policy)
        except ValueError:
            return

        if ( policy in (SAFE_POLICY, ALTERNATIVE_POLICY) and
             policy != self.getConflictPolicy() ):
            self._conflict_policy = policy
            self._clearQueues()

    security.declareProtected(manage_zcatalog_entries, 'getZCatalog')
    def getZCatalog(self, method=''):
        ZC = None
        REQUEST = getattr(self, 'REQUEST', None)
        cache = self._v_catalog_cache
        if cache is not None:
            # The cached catalog may be wrapped with an earlier
            # request.  Before using it, check the request.
            (ZC, req) = cache
            if req is not REQUEST:
                # It's an old wrapper.  Discard.
                ZC = None

        if ZC is None:
            if self._location is None:
                raise QueueConfigurationError(
                    "This QueueCatalog hasn't been "
                    "configured with a ZCatalog location."
                    )
            parent = aq_parent(aq_inner(self))
            try:
                ZC = parent.unrestrictedTraverse(self._location)
            except (KeyError, AttributeError):
                raise QueueConfigurationError(
                    "ZCatalog not found at %s." % self._location
                    )
            if not hasattr(ZC, 'getIndexObjects'): # XXX need a better check
                raise QueueConfigurationError(
                    "The object at %s does not implement the "
                    "IZCatalog interface." % self._location
                    )

            security_manager = getSecurityManager()
            if not security_manager.validate(self, self, self._location, ZC):
                raise Unauthorized(self._location, ZC)

            ZC = aq_base(ZC).__of__(parent)
            self._v_catalog_cache = (ZC, REQUEST)

        if method:
            if not _is_zcatalog_method(method):
                raise AttributeError(method)
            m = getattr(ZC, method)
            # Note that permission to access the method may be checked
            # later on.  This isn't the right place to check permission.
            return m
        else:
            return ZC

    def __getattr__(self, name):
        # The original object must be wrapped, but self isn't, so
        # we return a special object that will do the attribute access
        # on a wrapped object.
        if _is_zcatalog_method(name):
            return AttrWrapper(name)

        raise AttributeError(name)

    def _update(self, uid, etype):
        t = time()
        self._queues[hash(uid) % self._buckets].update(uid, etype)

    security.declareProtected(manage_zcatalog_entries, 'catalog_object')
    def catalog_object(self, obj, uid=None, idxs=None, update_metadata=1):
        # update_metadata=0 is ignored if the queued catalog is set to
        # update metadata during queue processing, rather than immediately

        # similarly, limiting the idxs only limits the immediate indexes.  If 
        # any work needs to be done in the queue processing, it will all be
        # done: we have not implemented partial indexing during queue 
        # processing.  The only way to avoid any of it is to avoid all of it 
        # (i.e., update metadata immediately and don't have any indexes to 
        # update on the queued side).

        # Make sure the current context is allowed to do this:
        catalog_object = self.getZCatalog('catalog_object')

        if uid is None:
            uid = '/'.join(obj.getPhysicalPath())
        elif not isinstance(uid, StringType):
            uid = '/'.join(uid)

        catalog = self.getZCatalog()
        cat_indexes = sets.Set(catalog.indexes())
        immediate_indexes = sets.Set(self._immediate_indexes)
        cat_indexes -= immediate_indexes

        # The ZCatalog API doesn't allow us to distinguish between
        # adds and updates, so we have to try to figure this out
        # ourselves.

        # There's a risk of a race here. What if there is a previously
        # unprocessed add event? If so, then this should be a changed
        # event. If we undo this transaction later, we'll generate a
        # remove event, when we should generate an add changed event.
        # To avoid this, we need to make sure we see consistent values
        # of the event queue. We also need to avoid resolving
        # (non-undo) conflicts of add events. This will slow things
        # down a bit, but adds should be relatively infrequent.

        # Now, try to decide if the catalog has the uid (path).
        already_cataloged = cataloged(catalog, uid)
        if not already_cataloged:
            # Looks like we should add, but maybe there's already a
            # pending add event. We'd better check the event queue:
            already_cataloged = (
                self._queues[hash(uid) % self._buckets].getEvent(uid) in
                ADDED_EVENTS)

        if idxs and already_cataloged:
            # if not already_cataloged, we index the whole thing
            idxs = sets.Set(idxs)
            immediate_indexes.intersection_update(idxs)
            cat_indexes.intersection_update(idxs)

        immediate_metadata = self.getImmediateMetadataUpdate()
        if cat_indexes or update_metadata and not immediate_metadata:
            self._update(uid, already_cataloged and CHANGED or ADDED)

        if immediate_indexes:
            # Update some of the indexes immediately.
            catalog.catalog_object(
                obj, uid, immediate_indexes,
                update_metadata=update_metadata and immediate_metadata)
        elif update_metadata and immediate_metadata:
            # if it is added, no point in doing the metadata, and it will be
            # done in the queue process anyway
            catalog._catalog.updateMetadata(obj, uid)

    security.declareProtected(manage_zcatalog_entries, 'uncatalog_object')
    def uncatalog_object(self, uid):
        if not isinstance(uid, StringType):
            uid = '/'.join(uid)

        self._update(uid, REMOVED)

        if self._immediate_removal:
            self._process_queue( self._queues[hash(uid) % self._buckets]
                               , limit=None
                               )

    security.declareProtected(manage_zcatalog_entries, 'process')
    def process(self, max=None):
        """ Process pending events and return number of events processed. """
        if not self.manage_size():
            return 0

        count = 0
        for queue in filter(None, self._queues):
            limit = None
            if max:
                # limit the number of events
                limit = max - count
        
            count += self._process_queue(queue, limit)

            if max and count >= max:
                # On reaching the maximum, return immediately
                # so the caller can commit the transaction,
                # sleep for a while, or do something else.
                break

        return count

    def _process_queue(self, queue, limit):
        """Process a single queue"""
        catalog = self.getZCatalog()

        if self.getProcessAllIndexes():
            idxs = None
        else:
            cat_indexes = sets.Set(catalog.indexes())
            immediate_indexes = sets.Set(self._immediate_indexes)
            if not immediate_indexes or immediate_indexes==cat_indexes:
                idxs = None # do all of 'em
            else:
                idxs = list(cat_indexes - immediate_indexes)
        events = queue.process(limit)
        count = 0

        for uid, (t, event) in events.items():
            if event is REMOVED:
                try:
                    if cataloged(catalog, uid):
                        catalog.uncatalog_object(uid)
                except (ConflictError, ClientDisconnected):
                    raise
                except:
                    logger.error('error uncataloging object', exc_info=True)
            else:
                # add or change
                if event is CHANGED and not cataloged(catalog, uid):
                    continue
                # Note that the uid may be relative to the catalog.
                obj = catalog.unrestrictedTraverse(uid, None)
                if obj is not None:
                    immediate_metadata = self.getImmediateMetadataUpdate()
                    try:
                        catalog.catalog_object(
                            obj, uid, idxs=idxs,
                            update_metadata=not immediate_metadata)
                    except (ConflictError, ClientDisconnected):
                        raise
                    except:
                        logger.error('error cataloging object', exc_info=True)

            count = count + 1

        return count
        

    #
    # CMF catalog tool methods.
    #
    security.declarePrivate('indexObject')
    def indexObject(self, object):
        """Add to catalog.
        """
        self.catalog_object(object, self.uidForObject(object))

    security.declarePrivate('unindexObject')
    def unindexObject(self, object):
        """Remove from catalog.
        """
        self.uncatalog_object(self.uidForObject(object))

    security.declarePrivate('reindexObject')
    def reindexObject(self, object, idxs=None,update_metadata=1,uid=None):
        """Update catalog after object data has changed.

        The optional idxs argument is a list of specific indexes
        to update (all of them by default).
        """
        self.catalog_object(object, uid or self.uidForObject(object), idxs=idxs,
                            update_metadata=update_metadata)

    security.declarePrivate('uidForObject')
    def uidForObject(self, obj):
        """Get a catalog uid for the object. Allows the underlying catalog
        to determine the uids if it implements this method"""
        catalog = self.getZCatalog()
        if hasattr(aq_base(catalog), 'uidForObject'):
            return catalog.uidForObject(obj)
        return '/'.join(obj.getPhysicalPath())

    # Provide web pages. It would be nice to use views, but Zope 2.6
    # just isn't ready for views. :( In particular, we'd have to fake
    # out the PageTemplateFiles in some brittle way to make them do
    # the right thing. :(

    security.declareProtected(view_management_screens, 'manage_editForm')
    manage_editForm = PageTemplateFile('www/edit', globals())

    security.declareProtected(view_management_screens, 'manage_getLocation')
    def manage_getLocation(self):
        return self._location or ''

    security.declareProtected(view_management_screens, 'manage_edit')
    def manage_edit(self, title='', location='', immediate_indexes=(),
                    immediate_removal=0, bucket_count=0, immediate_metadata=0,
                    all_indexes=0, conflict_policy=SAFE_POLICY, RESPONSE=None):
        """ Edit the instance """
        self.title = title
        self.setLocation(location or None)
        self.setImmediateIndexes(immediate_indexes)
        self.setImmediateRemoval(immediate_removal)
        self.setImmediateMetadataUpdate(immediate_metadata)
        self.setProcessAllIndexes(all_indexes)
        self.setConflictPolicy(conflict_policy)
        if bucket_count:
            bucket_count = int(bucket_count)
            if bucket_count != self.getBucketCount():
                self.setBucketCount(bucket_count)

        if RESPONSE is not None:
            RESPONSE.redirect('%s/manage_editForm?manage_tabs_message='
                              'Properties+changed' % self.absolute_url())


    security.declareProtected(manage_zcatalog_entries,
        'list_queue_items')
    def list_queue_items(self, limit=100):
        """Return a list of items in the queue."""
        items = []
        count = 0
        for queue in filter(None, self._queues):
            qitems = queue._data.keys()
            count += len(qitems)
            items += qitems
        if limit is not None:
            if count > limit:
                items = items[:limit]
        return items


    security.declareProtected(manage_zcatalog_entries, 'manage_queue')
    manage_queue = DTMLFile('dtml/queue', globals())

    security.declareProtected(manage_zcatalog_entries, 'manage_size')
    def manage_size(self):
        size = 0
        for q in self._queues:
            size += len(q)

        return size

    security.declareProtected(manage_zcatalog_entries, 'manage_process')
    def manage_process(self, count=100, REQUEST=None):
        "Web UI to manually process queues"
        count = int(count)
        processed = self.process(max=count)
        if REQUEST is not None:
            msg = '%i Queue item(s) processed' % processed
            return self.manage_queue(manage_tabs_message=msg)
        else:
            return processed

    # Provide Zope 2 offerings

    index_html = None

    meta_type = 'ZCatalog Queue'

    manage_options=(
        (
        {'label': 'Configure', 'action': 'manage_editForm',
         'help':('QueueCatalog','QueueCatalog-Configure.stx')},

        {'label': 'Queue', 'action': 'manage_queue',
         'help':('QueueCatalog','QueueCatalog-Queue.stx')},
        )
        +SimpleItem.manage_options
        )

    security.declareObjectPublic()
    # Disallow access to subobjects with no security assertions.
    security.setDefaultAccess('deny')

    security.declarePublic('getTitle', 'title_or_id')

    security.declareProtected(manage_zcatalog_entries,
                              'catalog_object', 'uncatalog_object')


def cataloged(catalog, path):
    getrid = getattr(catalog, 'getrid', None)
    if getrid is None:

        # This is an old catalog that doesn't provide an API for
        # getting an objects rid (and thus determing that the
        # object is already cataloged.

        # We'll just use our knowledge of the internal structure.

        rid = catalog._catalog.uids.get(path)

    else:
        rid = catalog.getrid(path)

    return rid is not None

class AttrWrapper(Base):
    "Special object that allowes us to use acquisition in QueueCatalog "
    "attribute access"

    def __init__(self, name):
        self.__name__ = name

    def __of__(self, wrappedQueueCatalog):
        return wrappedQueueCatalog.getZCatalog(self.__name__)

__doc__ = QueueCatalog.__doc__ + __doc__

