from django.db import models

class NoFillerManager(models.Manager):
    def get_queryset(self):
        return super(NoFillerManager, self).get_queryset().exclude(type='filler')