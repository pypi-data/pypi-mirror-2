from stdnet.utils import jsonPickler
from stdnet.backends.base import BaseBackend, ImproperlyConfigured, novalue
from stdnet.backends.structures.structredis import List,Set,HashTable,Map

try:
    import redis
except:
    raise ImproperlyConfigured("Redis cache backend requires the 'redis' library. Do easy_install redis")

try:
    import cPickle as pickle
except ImportError:
    import pickle

#default_pickler = jsonPickler()
default_pickler = pickle


class BackEnd(BaseBackend):
    '''Redis backend for StdNet. This is the backend to use really.'''
    def __init__(self, name, server, params, pickler = default_pickler):
        super(BackEnd,self).__init__(name,params)
        servs = server.split(':')
        server = servs[0]
        port   = 6379
        if len(server) == 2:
            port = int(servs[1])
        self.pickler         = pickler
        self.params          = params
        self.db              = params.pop('db',0)
        cache                = redis.Redis(host = server, port = port, db = self.db)
        self._cache          = cache
        self.execute_command = cache.execute_command
        self.incr      = cache.incr
        self.sismember = cache.sismember
        self.smembers  = cache.smembers
        self.zlen      = cache.zcard
        self.clear     = cache.flushdb
        self.sinter    = cache.sinter
    
    def set_timeout(self, id, timeout):
        timeout = timeout or self.default_timeout
        if timeout:
            self.execute_command('EXPIRE', id, timeout)
    
    def has_key(self, id):
        return self.execute_command('EXISTS', id)
    
    def set(self, id, value, timeout = None):
        value = self._val_to_store_info(value)
        r = self._cache.set(id,value)
        self.set_timeout(id,timeout)
        return r
    
    def get(self, id):
        res = self.execute_command('GET', id)
        return self._res_to_val(res)        
        
    def delete_object(self, meta):
        '''Delete an object from the database'''
        hash = self.hash(meta.basekey())
        id   = meta.id
        if not hash.delete(id):
            return 0
        for field in meta.fields.itervalues():
            if field.primary_key or not field.index:
                continue
            value = field.get_value(field._cleanvalue())
            fid   = meta.basekey(field.name,value)
            if field.unique:
                if not self.execute_command('DEL', fid):
                    raise Exception('could not delete unique index at %s' % fid)
            else:
                if not self.execute_command('SREM', fid, id):
                    raise Exception('could not delete index at set %s' % fid)
        return 1
    
    def list(self, id, timeout = 0):
        return List(self,id,timeout)
    
    def unordered_set(self, id, timeout = 0):
        return Set(self,id,timeout)
    
    def hash(self, id, timeout = 0):
        return HashTable(self,id,timeout)
    
    def map(self, id, timeout = 0):
        return Map(self,id,timeout)
    
    def _val_to_store_info(self, value):
        return self.pickler.dumps(value)
    
    def _res_to_val(self, res):
        if not res:
            return res
        try:
            return self.pickler.loads(res)
        except:
            return res
    
    # Hashes
    def hset(self, id, key, value):
        value = self._val_to_store_info(value)
        return self.execute_command('HSET', id, key, value)
    
    def hmset(self, id, mapping):
        items = []
        [items.extend((key,self._val_to_store_info(value))) for key,value in mapping.iteritems()]
        return self.execute_command('HMSET', id, *items)
    
    def hget(self, id, key):
        res = self.execute_command('HGET', id, key)
        return self._res_to_val(res)
    
        