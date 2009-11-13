from django.conf.urls.defaults import *

urlpatterns = patterns('wellknown.views',
    url(r'^\.well-known/(?P<path>.*)', 'handle', name='wellknown'),
    url(r'^crossdomain\.xml$', 'crossdomain', name='crossdomain.xml'),
    url(r'^robots\.txt$', 'robots', name='robots.txt'),
)
