from email.policy import default
from django.db import models
from django.contrib.auth.models import Group

class Description(models.Model):
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    current_stage = models.CharField(max_length=128)
    version = models.CharField(max_length=128)
    description = models.CharField(max_length=6000)
    model_author = models.CharField(max_length=128, null=True, blank=True )
    model_url = models.CharField(max_length=128)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.description
    