from django.db import models
from django.db.models.signals import post_save
import mimetypes
import wellknown

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
    wellknown._cache[reg.path] = (reg.content, reg.content_type)

post_save.connect(save_handler, sender=Resource)