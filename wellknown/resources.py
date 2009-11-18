from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

class HostMeta(object):
    
    def __init__(self):
        self._links = []
        self._hosts = getattr(settings, "WELLKNOWN_HOSTMETA_HOSTS", (Site.objects.get_current().domain,))
        self._lang = getattr(settings, "LANGUAGE_CODE", "en-us")
        
    def register_link(self, rels, uri=None, uri_template=None, title=None):
        
        if uri is None and uri_template is None:
            raise ValueError('one of uri or uri_template is required')
            
        link = {'rels': rels}
        if uri:
            link['uri'] = uri
        if uri_template:
            link['uri_template'] = uri_template
        if title:
            link['title'] = title
        
        self._links.append(link)
        
    def __call__(self, *args, **kwargs):
        data = {'hosts': self._hosts, 'links': self._links, 'lang': self._lang}
        return render_to_string('wellknown/host-meta.xml', data)