from django.db import models

# Create your models here.


class Photo(models.Model):
    url = models.CharField(u"url", max_length=128)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.url

    @models.permalink
    def get_absolute_url(self):
        return 'facer_input', (), {'pk': self.pk}