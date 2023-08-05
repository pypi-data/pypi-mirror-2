from stdnet.exceptions import *

novalue = object()


try:
    import cPickle as pickle
except ImportError:
    import pickle

#default_pickler = jsonPickler()
default_pickler = pickle

class NoPickle(object):
    
    def loads(self, s):
        return s
    
    def dumps(self, obj):
        return obj

nopickle = NoPickle()


class Pipeline(object):
    
    def __init__(self, pipe, method):
        self.pipe   = pipe
        self.method = method


class BaseBackend(object):
    '''Generic interface for a backend database:
    
    * *name* name of database, such as **redis**, **couchdb**, etc..
    * *params* dictionary of configuration parameters
    * *pickler* calss for serializing and unserializing data. It must implement the *loads* and *dumps* methods.
    '''
    def __init__(self, name, params, pickler = None):
        self.__name = name
        timeout = params.get('timeout', 0)
        try:
            timeout = int(timeout)
        except (ValueError, TypeError):
            timeout = 0
        self.default_timeout = timeout
        self._cachepipe = {}
        self._keys      = {}
        self.fields     = []
        self.params     = params
        self.pickler    = pickler or default_pickler

    @property
    def name(self):
        return self.__name
    
    def __repr__(self):
        return '%s backend' % self.__name
    
    def __str__(self):
        return self.__repr__()
    
    def createdb(self, name):
        pass
    
    def get_object(self, meta, name, value):
        '''Retrive an object from the database. If object is not available, it raise
and :ref:`ObjectNotFund <utility-exceptions>` exception.

    * *meta* :ref:`database metaclass <database-metaclass>` or model
    * *name* name of field (must be unique)
    * *value* value of field to search.'''
        if name != 'id':
            value = self._get(meta.basekey(name,value))
        if value is None:
            raise ObjectNotFund
        value = self.hash(meta.basekey()).get(value)
        if value is None:
            raise ObjectNotFund
        return value
    
    def add_object(self, obj, commit = True):
        '''Add a model object to the database:
        
        * *obj* instance of :ref:`StdModel <model-model>` to add to database
        * *commit* If True, *obj* is saved to database, otherwise it remains in local cache.
        '''
        meta   = obj._meta
        id     = meta.basekey()
        cache  = self._cachepipe
        cvalue = cache.get(id,None)
        if cvalue is None:
            cvalue = Pipeline({},'hash')
            cache[id] = cvalue
        hash = self.hash(id, meta.timeout, cvalue.pipe)
        objid = obj.id
        hash.add(objid, obj)
        
        # Create indexes if possible
        for name,field in meta.fields.items():
            if name is 'id':
                continue
            if field.index:
                value   = field.hash(field.serialize())
                key     = meta.basekey(field.name,value)
                if field.unique:
                    self._keys[key] = objid
                elif field.ordered:                    
                    cvalue = cache.get(key,None)
                    if cvalue is None:
                        cvalue = Pipeline(set(),'ordered_set')
                        cache[key] = cvalue
                    index = self.ordered_set(key,
                                             timeout  = meta.timeout,
                                             pipeline = cvalue.pipe,
                                             pickler  = nopickle)
                    index.add(objid)
                else:
                    cvalue = cache.get(key,None)
                    if cvalue is None:
                        cvalue = Pipeline(set(),'unordered_set')
                        cache[key] = cvalue
                    index = self.unordered_set(key,
                                               timeout  = meta.timeout,
                                               pipeline = cvalue.pipe,
                                               pickler  = nopickle)
                    index.add(objid)
            
            savefield = getattr(field,'save',None)
            if savefield:
                self.fields.append(savefield)
                
        if commit:
            self.commit()
            
    def commit(self):
        '''Commit cache objects to backend database'''
        for id,cvalue in self._cachepipe.iteritems():
            el = getattr(self,cvalue.method)(id, pipeline = cvalue.pipe)
            el.save()
        if self._keys:
            self._set_keys()
            self._keys.clear()
        for save in self.fields:
            save()
        self.fields = []            
            
    def delete_object(self, obj):
        '''Delete an object from the database'''
        meta   = obj._meta
        id     = meta.basekey()
        hash   = self.hash(id)
        if not hash.delete(obj.id):
            return 0
        self.delete_indexes(obj)
        return 1
    
    def delete_indexes(self, obj):
        pass
    
    def set(self, id, value, timeout = None):
        value = self.pickler.dumps(value)
        return self._set(id,value,timeout)
    
    def get(self, id, default = None):
        v = self._get(id)
        if v:
            return self.pickler.loads(v)
        else:
            return default

    def get_many(self, keys):
        """
        Fetch a bunch of keys from the cache. For certain backends (memcached,
        pgsql) this can be *much* faster when fetching multiple values.

        Returns a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.
        """
        d = {}
        for k in keys:
            val = self.get(k)
            if val is not None:
                d[k] = val
        return d

    def has_key(self, key):
        """
        Returns True if the key is in the cache and has not expired.
        """
        return self.get(key) is not None

    def incr(self, key, delta=1):
        """
        Add delta to value in the cache. If the key does not exist, raise a
        ValueError exception.
        """
        if key not in self:
            raise ValueError("Key '%s' not found" % key)
        new_value = self.get(key) + delta
        self.set(key, new_value)
        return new_value

    def decr(self, key, delta=1):
        """
        Subtract delta from value in the cache. If the key does not exist, raise
        a ValueError exception.
        """
        return self.incr(key, -delta)

    def __contains__(self, key):
        """
        Returns True if the key is in the cache and has not expired.
        """
        # This is a separate method, rather than just a copy of has_key(),
        # so that it always has the same functionality as has_key(), even
        # if a subclass overrides it.
        return self.has_key(key)



    def delete_many(self, keys):
        """
        Set a bunch of values in the cache at once.  For certain backends
        (memcached), this is much more efficient than calling delete() multiple
        times.
        """
        for key in keys:
            self.delete(key)

    def clear(self):
        """Remove *all* values from the database at once."""
        raise NotImplementedError

    # VIRTUAL METHODS
    
    def _set(self, id, value, timeout):
        raise NotImplementedError
    
    def _get(self, id):
        raise NotImplementedError
    
    def _set_keys(self):
        raise NotImplementedError
            
    # DATASTRUCTURES
    
    def list(self, *args, **kwargs):
        '''Return an instance of :ref:`List <list-structure>`
        for a given *id*.'''
        raise NotImplementedError
    
    def hash(self, *args, **kwargs):
        '''Return an instance of :ref:`HashTable <hash-structure>`
        for a given *id*.'''
        raise NotImplementedError
    
    def unordered_set(self, *args, **kwargs):
        '''Return an instance of :ref:`Set <set-structure>`'''
        raise NotImplementedError
    
    def ordered_set(self, *args, **kwargs):
        '''Return an instance of :ref:`Ordered Set <orderedset-structure>`'''
        raise NotImplementedError
    

