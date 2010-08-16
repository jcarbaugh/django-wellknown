from django.template.loader import render_to_string
import mimetypes

from wellknown.resources import HostMeta

_cache = { }

def get_hostmeta():
    return get_resource('host-meta')[0]

def get_resource(path):
    return _cache.get(path, (None, None))

def register(path, handler=None, template=None, content=None, content_type=None, update=False):
    
    if path in _cache:
        raise ValueError(u"duplicate resource for %s" % path)
        
    if content_type is None and not update:
        content_type = mimetypes.guess_type(path)[0] or 'text/plain'
        
    if handler:
        _cache[path] = (handler, content_type)
    elif template:
        _cache[path] = (render_to_string(template), content_type)
    elif content:
        _cache[path] = (content, content_type)
    else:
        raise ValueError(u"either handler, template, or content must be specified")

__all__ = ['register','get_resource','get_hostmeta']

# register default host-meta handler.
register('host-meta', handler=HostMeta(),
         content_type='application/xrd+xml')
