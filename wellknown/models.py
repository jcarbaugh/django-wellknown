from django.db import models
from django.db.models.signals import post_save
from wellknown import hostmeta, register
import mimetypes

class Resource(models.Model):
    path = models.CharField(max_length=128)
    content = models.TextField(blank=True)
    content_type = models.CharField(max_length=128, blank=True)
    
    class Meta:
        ordering = ('path',)
    
    def __unicode__(self):
        return self.path
    
    def save(self, **kwargs):
        self.path = self.path.strip('/')
        if not self.content_type:
            self.content_type = mimetypes.guess_type(self.path)[0] or 'text/plain'
        super(Resource, self).save(**kwargs)

#
# update resources when models are saved
#

def save_handler(sender, **kwargs):
    reg = kwargs['instance']
    register(
        reg.path,
        content=reg.content,
        content_type=reg.content_type,
        update=True
    )

post_save.connect(save_handler, sender=Resource)

#
# cache resources
#

for res in Resource.objects.all():
    register(res.path, content=res.content, content_type=res.content_type)

#
# create default host-meta handler
#

register('host-meta', handler=hostmeta, content_type='application/xrd+xml')
