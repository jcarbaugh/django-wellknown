from django.template.loader import render_to_string
import mimetypes

_cache = { }

def register(path, handler=None, template=None, content=None, content_type=None):
    
    if path in _cache:
        raise ValueError(u"duplicate registration for %s" % path)
        
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
    from wellknown.models import Registration
    for reg in Registration.objects.all():
        register(reg.path, content=reg.content, content_type=reg.content_type)