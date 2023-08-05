# Copyright 2009-2010, BlueDynamics Alliance - http://bluedynamics.com
import uuid
import random
from zope.interface import implements
from zope.component import getUtility
from zope.annotation import IAnnotations
from Acquisition import (
    aq_inner,
    aq_parent,
)
from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem
from interfaces import (
    ISoupAnnotatable,
    ISoup,
    IRecord,
    ICatalogFactory
)

class NoLongerSupported(Exception): pass

class StorageLocator(object):
    
    def __init__(self, context):
        self.context = context
    
    @property
    def root(self):
        obj = aq_inner(self.context)
        while True:
            if ISoupAnnotatable.providedBy(obj):
                return obj
            obj = aq_parent(obj)
            if not obj:
                raise AttributeError(u"Invalid soup context.")
    
    def storage(self, id):
        return self.locate(id)
    
    def path(self, id):
        annotations = IAnnotations(self.root)
        if isinstance(annotations[id], basestring):
            return annotations[id]
        return '/'
    
    def traverse(self, path):
        obj = self.root
        path = path.split('/')
        for name in path:
            try:
                obj = obj[name]
            except AttributeError, e:
                msg = u'Object at %s does not exist.' % '/'.join(path)
                raise ValueError(msg)
        return obj
    
    def annotated(self, obj, id):
        annotations = IAnnotations(obj)
        if not id in annotations:
            annotations[id] = SoupData()
        return annotations[id]
    
    def locate(self, id):
        entity = self.annotated(self.root, id)
        if isinstance(entity, basestring):
            entity = self.annotated(self.traverse(entity), id)
        if isinstance(entity, SoupData):
            return entity
        msg = u'Conflicting annotation with name %s. No SoupData contained'
        msg = msg % id
        raise ValueError(msg)
    
    def move(self, id, path):
        storage = self.storage(id)
        target = self.traverse(path)
        annotations = IAnnotations(target)
        annotations[id] = storage
        annotations = IAnnotations(self.root)
        annotations[id] = path

class SoupData(SimpleItem):
    
    def __init__(self):
        self.data = IOBTree()
        self.catalog = None

def getSoup(context, id):
    return Soup(context, id)

#class Soup(object): XXX: 2.1
class Soup(SimpleItem):
    implements(ISoup)
    
    def __init__(self, context, id):
        self.context = context
        self.id = id
    
    @property
    def storage(self):
        if not hasattr(self, 'context'):
            error = u'Using ISoup as utility is no longer supported. ' + \
                    u'Register your Soup as adapter instead and change the ' + \
                    u'soup lookups in your code.'
            raise NoLongerSupported(error)
        request = self.context.REQUEST
        cachekey = 'soup_storage_%s' % self.id
        if request.get(cachekey):
            return request[cachekey]
        storage = StorageLocator(self.context).storage(self.id)
        request[cachekey] = storage
        return storage
    
    @property
    def data(self):
        return self.storage.data
    
    @property
    def catalog(self):
        storage = self.storage
        if not storage.catalog:
            storage.catalog = getUtility(ICatalogFactory, name=self.id)()
        return storage.catalog

    def add(self, record):
        record.intid = self._generateid()
        self.data[record.intid] = record
        record = self.data[record.intid] # ?
        self.catalog.index_doc(record.intid, record)
        # XXX: notify subscribers here if not done by OFS, check this.
        return record.intid
    
    def _query(self, **kw):
        querykw = {}
        for key in kw:
            if isinstance(kw[key], list) \
              or isinstance(kw[key], tuple):
                assert(len(kw[key]) == 2)
                querykw[key] = kw[key]
            else:
                querykw[key] = (kw[key], kw[key])
        return self.catalog.apply(querykw)
    
    def query(self, **kw):
        ids = self._query(**kw)
        for id in ids:
            yield self.data[id]
    
    def lazy(self, **kw):
        ids = self._query(**kw)
        for id in ids:
            yield LazyRecord(id, self)
    
    def rebuild(self):
        self.storage.catalog = getUtility(ICatalogFactory, name=self.id)()
        self.reindex()
    
    def reindex(self, records=None):
        if records is None:
            records = self.data.values()
        for record in records:
            self.catalog.index_doc(record.intid, record)

    def __delitem__(self, record):
        try:
            del self.data[record.intid]
        except Exception, e:
            raise e
            #raise ValueError(u"Record not contained in this soup")
        self.catalog.unindex_doc(record.intid)
    
    _v_nextid = None
    _randrange = random.randrange
    
    def _generateid(self):
        # Stolen from zope.app.intid.
        while True:
            if self._v_nextid is None:
                self._v_nextid = self._randrange(0, 2**31)
            uid = self._v_nextid
            self._v_nextid += 1
            if uid not in self.data:
                return uid
            self._v_nextid = None

class LazyRecord(object):
    
    def __init__(self, intid, soup):
        self.intid = intid
        self.soup = soup
    
    def __call__(self):
        return self.soup.data[self.intid]

EMPTY_MARKER = object()

class Record(SimpleItem):
    implements(IRecord)
    
    def __init__(self, **kw):
        self.id = uuid.uuid4().hex
        self.intid = None
        self.data = OOBTree()
        for key in kw.keys():
            self.data[key] = kw[key]
        self._p_changed = True
    
    def __getattribute__(self, name):
        try:
            attr = SimpleItem.__getattribute__(self, 'data').get(name,
                                                                 EMPTY_MARKER)
            if attr is not EMPTY_MARKER:
                return attr
        except AttributeError, e:
            pass
        return SimpleItem.__getattribute__(self, name)