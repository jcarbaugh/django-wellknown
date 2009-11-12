from django.http import HttpResponse, Http404
import wellknown

try:
    from robots.views import rules_list
except ImportError:
    rules_list = None

def handle(request, path, *args, **kwargs):

    (handler_or_content, content_type) = wellknown._cache.get(path, (None, None))

    if handler_or_content is None:
        raise Http404()

    if callable(handler_or_content):
        content = handler_or_content(request, path, content_type=content_type, *args, **kwargs)
    else:
        content = handler_or_content

    return HttpResponse(content or '', content_type=content_type)

def crossdomain(request, *args, **kwargs):
    return handle(request, 'crossdomain.xml', *args, **kwargs)

def robots(request, *args, **kwargs):
    if rules_list:  # use django-robots if it is installed
        return rules_list(request, *args, **kwargs)
    return handle(request, 'robots.txt', *args, **kwargs)