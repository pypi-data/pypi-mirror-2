from uuid import uuid4
import json

from stdnet.utils import zip, iteritems, to_bytestring
from stdnet.exceptions import FieldError, ObjectNotFound

from .base import nopickle
from .redisb import BackendDataServer as BackendDataServer0

def gen_unique_id():
    return str(uuid4())


class BackendDataServer(BackendDataServer0):
    '''A new Redis backend'''
    
    def unwind_query(self, meta, qset):
        table = meta.table()
        ids = list(qset)
        make_object = self.make_object
        for id,data in zip(ids,table.mget(ids)):
            yield make_object(meta,id,data)            
        
    def idset(self, meta):
        return self.unordered_set(meta.basekey('id'), pickler = nopickle)
    
    def instance_keys(self, obj):
        meta = obj._meta
        if meta.multifields:
            keys = []
            for field in meta.multifields:
                f = getattr(obj,field.attname)
                keys.append(f.id)
            return keys
        else:
            return ()
    
    def _unique_set(self, meta, idset, name, values, check = True):
        '''Handle filtering over unique fields'''
        uset = set()
        if name == 'id':
            for id in values:
                if not check or id in idset:
                    uset.add(to_bytestring(id))
        else:
            for value in values:
                bkey = meta.basekey(name,value)
                id = self._get(bkey)
                if id:
                    uset.add(to_bytestring(id))
        return uset
        
    def query(self, meta, fargs, eargs, filter_sets = None):
        # QUERY a model
        #
        # fargs is a dictionary of filters
        # eargs is a dictionary of excludes
        # filter_sets are ids from fields
        #
        qset = None
        temp_ids = []
        idset = self.idset(meta)
            
        filters = None
        if fargs:
            filters = []
            for name,data in iteritems(fargs):
                values,unique = data
                if unique:
                    uset = self._unique_set(meta, idset, name, values)
                    if not uset:
                        return uset
                    if qset is None:
                        qset = uset
                    else:
                        qset = qset.intersection(uset)
                        if not qset:
                            return qset
                elif values:
                    if len(values) == 1:
                        filters.append(meta.basekey(name,values[0]))
                    else:
                        insersept = [meta.basekey(name,value) for value in values]
                        id = gen_unique_id()
                        temp_ids.append(id)
                        self.sunionstore(id,insersept)
                        filters.append(id)
                    
        if filters or filter_sets:
            if filters and filter_sets:
                filters.extend(filter_sets)
            elif not filters:
                filters = filter_sets
                
            v = self.sinter(filters)
            if qset:
                qset.intersection(v)
            else:
                qset = v
            
            if not qset:
                return qset
            
        if eargs:
            excludes = []
            euset = set()
            for name,data in iteritems(eargs):
                values,unique = data
                if unique:
                    euset = euset.union(self._unique_set(meta, idset, name, values, check = False))
                else:
                    if len(values) == 1:
                        excludes.append(meta.basekey(name,values[0]))
                    else:
                        insersept = [meta.basekey(name,value) for value in values]
                        id = gen_unique_id()
                        temp_ids.append(id)
                        self.sunionstore(id,insersept)
                        excludes.append(id)
                        
            if excludes:
                excludes.insert(0,idset.id)
                eset  = self.sdiff(excludes)
                if qset:
                    qset = qset.intersection(eset)
                else:
                    qset = eset
            elif qset is None:
                qset = set(idset)
                
            if euset:
                qset -= euset
        
        if qset is None:
            qset = idset
            
        if temp_ids:
            self.delete(*temp_ids)
        return qset
    
    def make_object(self, meta, id , data):
        obj = meta.maker()
        obj.__setstate__((id,data))
        return obj
    
    def get_object(self, meta, name, value):
        if name != 'id':
            id = self._get(meta.basekey(name,value))
        else:
            id = value
        if id is None:
            raise ObjectNotFound
        hash = meta.table()
        data = hash.get(id)
        if data is None:
            raise ObjectNotFound
        return self.make_object(meta, id, data)
            
    def save_object(self, obj, commit):
        # Save the object in the back-end
        meta = obj._meta
        timeout = meta.timeout
        if not obj.is_valid():
            raise FieldError(json.dumps(obj.errors))
        data = obj.cleaned_data
        objid = obj.id
        #
        # if editing (id already available) we need to clear the previous element.
        # But not its related objects.
        if objid:
            try:
                pobj = obj.__class__.objects.get(id = objid)
                self.delete_object(pobj, multi_field = False)
            #TODO: we should use this except but it fails ManyToMany field to fail tests
            #except obj.DoesNotExist:
            except:
                pass
        objid = obj.id = meta.pk.serialize(objid)
        
        # Add object data to the model hash table
        hash = meta.table()
        hash.add(objid, data)
        bkey = meta.basekey
        
        # Add id to id set
        index = self.unordered_set(bkey('id'), timeout, pickler = nopickle)
        index.add(objid)
        
        # Create indexes if possible
        for field,value in obj.indices:
            key = bkey(field.name,value)
            if field.unique:
                index = self.index_keys(key, timeout)
            else:
                if field.ordered:
                    index = self.ordered_set(key, timeout, pickler = nopickle)
                else:
                    index = self.unordered_set(key, timeout, pickler = nopickle)
            index.add(objid)
                
        if commit:
            self.commit()
        
        return obj
    
    def delete_object(self, obj, deleted = None, multi_field = True):
        append  = None if deleted is None else deleted.append
        meta    = obj._meta
        timeout = meta.timeout
        hash    = meta.table()
        bkey    = meta.basekey
        objid   = obj.id
        
        # Remove object from model hash table
        if not hash.delete(objid):
            return 0
        
        # ids set
        sid = bkey('id')
        index = self.unordered_set(sid, timeout, pickler = nopickle)
        if index.discard(objid) and append:
            append(sid)
        
        for field in meta.fields:
            name = field.name
            if field.index:
                key = bkey(name,field.serialize(getattr(obj,name,None)))
                if field.unique:
                    if self.delete(key) and append:
                        deleted.append(key)
                else:
                    if field.ordered:
                        index = self.ordered_set(key, timeout, pickler = nopickle)
                    else:
                        index = self.unordered_set(key, timeout, pickler = nopickle)
                    index.discard(objid)
            fid = field.id(obj)
            if fid and multi_field:
                if self.delete(fid) and append:
                    append(fid)
        return 1
