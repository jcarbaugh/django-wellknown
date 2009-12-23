from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from xrd import XRD, Link, Element

LANGUAGE_CODE = getattr(settings, "LANGUAGE_CODE", "en-us")

class HostMeta(XRD):
    
    def __init__(self):
        
        super(HostMeta, self).__init__()
        
        self.attributes.append(('xmlns:hm','http://host-meta.net/ns/1.0'))
        
        hosts = getattr(settings, "WELLKNOWN_HOSTMETA_HOSTS", (Site.objects.get_current().domain,))
        for host in hosts:
            self.elements.append(Element('hm:Host', host))
        
    def register_link(self, rel, href=None, template=None, title=None):
        
        if href is None and template is None:
            raise ValueError('one of href or template is required')
            
        link = Link(rel=rel, href=href, template=template)
        if title:
            link.titles.append(title)
            
        self.links.append(link)
        
    def __call__(self, *args, **kwargs):
        data = {'hosts': self._hosts, 'links': self._links}
        return self.to_xml()