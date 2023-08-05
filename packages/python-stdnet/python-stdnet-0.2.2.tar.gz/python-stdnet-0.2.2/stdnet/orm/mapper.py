import copy
from stdnet.main import getdb
from stdnet.conf import settings

from query import Manager    

def clear(backend = None):
    backend = backend or settings.DEFAULT_BACKEND
    cursor = getdb(backend)
    cursor.clear()
    
def clearall():
    for meta in _registry.values():
        meta.cursor.clear()

def register(model, backend = None, keyprefix = None, timeout = 0):
    backend = backend or settings.DEFAULT_BACKEND
    prefix  = keyprefix or model._meta.keyprefix or settings.DEFAULT_KEYPREFIX or ''
    if prefix:
        prefix = '%s:' % prefix
    meta    = model._meta
    meta.keyprefix = prefix
    meta.timeout   = timeout or 0
    objects = getattr(model,'objects',None)
    if not objects:
        objects = Manager()
    else:
        objects = copy.copy(objects)
    model.objects    = objects
    meta.cursor      = getdb(backend)
    objects.model    = model
    objects._meta    = meta
    objects.cursor   = meta.cursor
    _registry[model] = meta 
    

_registry = {}
