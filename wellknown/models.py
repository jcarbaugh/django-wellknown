from django.db import models
from django.db.models.signals import post_save
import mimetypes
import wellknown

#
# resource model
#

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
    wellknown.register(
        reg.path,
        content=reg.content,
        content_type=reg.content_type,
        update=True
    )

post_save.connect(save_handler, sender=Resource)
