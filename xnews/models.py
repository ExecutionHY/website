from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    introduction = models.CharField(max_length=128, default='This guy is too lazy to left anything.')

    def __unicode__(self):
        return self.id