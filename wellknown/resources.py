import re

from django.conf import settings
from django.template.loader import render_to_string
from xrd import XRD, Link, Element

LANGUAGE_CODE = getattr(settings, "LANGUAGE_CODE", "en-us")

class HostMeta(XRD):
    
    def __init__(self):
        
        super(HostMeta, self).__init__()
        
        self.attributes.append(('xmlns:hm','http://host-meta.net/ns/1.0'))
        
        hosts = getattr(settings, "WELLKNOWN_HOSTMETA_HOSTS", ('example.com',))
        for host in hosts:
            self.elements.append(Element('hm:Host', host))
        
    def __call__(self, *args, **kwargs):
        doc = self.to_xml()
        xml = doc.toprettyxml(indent='  ')
        expr = re.compile(r'>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
        return expr.sub(r'>\g<1></', xml)
