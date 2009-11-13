from django.template.loader import render_to_string
from wellknown.resources import HostMeta
import mimetypes

_cache = { }

hostmeta = HostMeta()

def register(path, handler=None, template=None, content=None, content_type=None):
    
    if path in _cache:
        raise ValueError(u"duplicate resource for %s" % path)
        
    if content_type is None:
        content_type = mimetypes.guess_type(path)[0] or 'text/plain'
        
    if handler:
        _cache[path] = (handler, content_type)
    elif template:
        _cache[path] = (render_to_string(template), content_type)
    elif content:
        _cache[path] = (content, content_type)
    else:
        raise ValueError(u"either handler, template, or content must be specified")
        
def init():
    from wellknown.models import Resource
    for res in Resource.objects.all():
        register(res.path, content=res.content, content_type=res.content_type)
    register('host-meta', handler=hostmeta.render, content_type='text/plain')