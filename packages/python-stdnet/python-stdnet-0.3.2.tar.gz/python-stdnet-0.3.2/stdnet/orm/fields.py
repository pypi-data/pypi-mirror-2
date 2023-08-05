from copy import copy
import time
from datetime import date, datetime

from query import RelatedManager
from stdnet.exceptions import *
from stdnet.utils import timestamp2date, date2timestamp



__all__ = ['Field',
           'AutoField',
           'AtomField',
           'DateField',
           'ForeignKey',
           '_novalue']

class NoValue(object):
    pass

_novalue = NoValue()


class Field(object):
    '''This is the base class of of StdNet Fields. The following arguments
    are available to all field types. All are optional.
    
    * **index** If True, the field will create indexes for fast search.
    * **unique** If True, this field must be unique throughout the model. If True index is also True. Enforced at database level.
    * **ordered** If True, the field is ordered (if unique is True this has no effect).
    * **primary_key** If True, this field is the primary key for the model. In this case the Field is also unique.
    * **required** If False, the field is allowed to be null.
    '''
    def __init__(self, unique = False, ordered = False, primary_key = False,
                 required = True, index = True):
        self.primary_key = primary_key
        if primary_key:
            self.unique   = True
            self.required = True
            self.index    = True
        else:
            self.unique = unique
            self.required = required
            if unique:
                self.index = True
            else:
                self.index = index
        self.ordered  = ordered
        self._value   = None
        self.obj      = None
        self.meta     = None
        self.name     = None
        self.model    = None
        
    def register_with_model(self, fieldname, model):
        pass
    
    def set_value(self, name, obj, value):
        # Called by constructor in the model
        self.obj  = obj
        self.name = name
        self.meta = obj._meta
        if not self.meta.cursor:
            raise ModelNotRegistered('Model %s is not registered with backend database' % self.meta.name)
        if value is not _novalue:
            self._value = value
        return self._value
    
    def get_full_value(self):
        '''Return the expanded value of the field. For standard fields this is the
        same as the field value, while for more complex fields, such as ForeignKey, it
        retrives extra data from the database. This function is called by the model when accessing
        fields values.'''
        return self._value
    
    def get_value(self, value):
        ''''''
        return value
    
    def hash(self, value):
        '''Internal function used to hash the value so it can be used as index'''
        return value
    
    def serialize(self):
        return self.get_value(self._value)
    
    def isvalid(self):
        '''Return ``True`` if Field is valid otherwise raise a ``FieldError`` exception.'''
        name    = self.name
        obj     = self.obj
        value   = self.serialize()
        if value is None and self.required:
            raise FieldError('Field %s for %s has no value' % (name,obj))
        if self.primary_key:
            setattr(obj,name,value)
        return True
    
    def add(self, *args, **kwargs):
        raise NotImplementedError("Cannot add to field")
    
    def delete(self):
        pass
    
    def __deepcopy__(self, memodict):
        '''Nothing to deepcopy here'''
        return copy(self)
            

class AtomField(Field):
    '''The simpliest field possible, it can be of four different types:

    * boolean
    * integer
    * floating point
    * string
    '''
    def hash(self, value):
        if isinstance(value,basestring):
            return hash(value)
        else:
            return value
    
    def set(self,obj,value):
        pass


class AutoField(Field):
    '''An integer only field that automatically increments. You usually won't
    need to use this directly;
    a primary key field will automatically be added to your model
    if you don't specify otherwise.
    '''
    def serialize(self):
        if not self._value:
            meta = self.meta
            self._value = meta.cursor.incr(meta.basekey('ids'))
        return self._value
    
    
class DateField(Field):
    '''A date, represented in Python by a datetime.date instance.
    '''
    def hash(self, value):
        if isinstance(value,date):
            return date2timestamp(value)
        else:
            return value
        
    def serialize(self):
        return self.hash(self._value)
    
    def set_value(self, name, obj, value):
        value = super(DateField,self).set_value(name,obj,value)
        if value and not isinstance(value,date):
            value = timestamp2date(value).date()
        self._value = value


class RelatedObject(object):
    
    def __init__(self,
                 model,
                 related_name = None,
                 relmanager = None):
        if not model:
            raise ValueError('Model not specified')
        self.model        = model
        self.related_name = related_name
        self.relmanager   = relmanager
    
    def register_related_model(self, name, related):
        if not self.model:
            return
        if self.model == 'self':
            self.model = related
        model = self.model
        meta  = model._meta
        related_name = self.related_name or '%s_set' % related._meta.name
        if related_name not in meta.related and related_name not in meta.fields:
            self.related_name = related_name
            manager = self.relmanager(related,name)
            meta.related[related_name] = manager
            return manager
        else:
            raise FieldError("Duplicated related name %s in model %s and field %s" % (related_name,related,name))


class ForeignKey(Field, RelatedObject):
    '''A field defining a one-to-many objects relationship.
The StdNet equivalent to `django ForeignKey <http://docs.djangoproject.com/en/dev/ref/models/fields/#foreignkey>`_.
Requires a positional argument: the class to which the model is related.
To create a recursive relationship, an object that has a many-to-one relationship with itself,
use::

    orm.ForeignKey('self')

It accepts **related_name** as extra argument. It is the name to use for the relation from the related object
back to self. For example::

    class Folder(orm.StdModel):
        name = orm.AtomField()
    
    class File(orm.StdModel):
        folder = orm.ForeignKey(Folder, related_name = 'files')
        
'''        
    def __init__(self, model, related_name = None, **kwargs):
        Field.__init__(self, **kwargs)
        RelatedObject.__init__(self,
                               model,
                               relmanager = RelatedManager,
                               related_name = related_name)
        self.__value_obj = _novalue
        self.index = True
        
    def register_with_model(self, name, related):
        self.register_related_model(name, related)
    
    def set_value(self, name, obj, value):
        value = super(ForeignKey,self).set_value(name,obj,value)
        if isinstance(value,self.model):
            self.__value_obj = value
            self._value = value.id
    
    def get_full_value(self):
        v = self.__value_obj
        if isinstance(v,NoValue):
            if self._value:
                meta    = self.model._meta
                hash    = meta.cursor.hash(meta.basekey())
                v       = hash.get(self._value)
            else:
                v = None
            self.__value_obj = v
        return v
    
    def get_value(self, value):
        if isinstance(value,self.model):
            return value.id
        else:
            return value
    
    def hash(self, value):
        return self.get_value(value)
    
    #def save_index(self, commit, value):
    #    meta    = self.meta
    #    name    = self.name
    #    obj     = self.obj
    #    key     = meta.basekey(name,value)
    #    return meta.cursor.add_index(key, obj.id, commit, timeout = meta.timeout)
    
        