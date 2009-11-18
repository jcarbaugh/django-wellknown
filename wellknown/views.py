from django.conf import settings
from django.http import HttpResponse, Http404
import wellknown

try:
    from robots.views import rules_list
except ImportError:
    rules_list = None

def handle(request, path, *args, **kwargs):
    """ Basic handler view to either display cached content
        or make call to actual handler method for rendering.
    """

    (handler_or_content, content_type) = wellknown.get_resource(path)

    if handler_or_content is None:
        raise Http404()

    if callable(handler_or_content):
        content = handler_or_content(request, content_type=content_type, *args, **kwargs)
    else:
        content = handler_or_content

    return HttpResponse(content or '', content_type=content_type)

def crossdomain(request, *args, **kwargs):
    """ View that overrides /crossdomain.xml to
        handle as a well-known resource.
    """
    return handle(request, 'crossdomain.xml', *args, **kwargs)

def robots(request, *args, **kwargs):
    """ Handle /robots.txt as a well-known resource or
        pass off request to django-robots.
    """
    if rules_list:  # use django-robots if it is installed
        return rules_list(request, *args, **kwargs)
    return handle(request, 'robots.txt', *args, **kwargs)