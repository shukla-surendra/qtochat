from django.db import models
from django.utils import timezone
import datetime
import uuid

class User(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    status   = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField('date created', default=timezone.now)

class Site(models.Model):
    site_name = models.CharField(max_length=100, default="default")
    site_token = models.CharField(max_length=150, default = uuid.uuid4().hex)
    site_url = models.CharField(max_length=100)
    site_type = models.CharField(max_length = 100, default="default")
    status   = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField('date created', default=timezone.now)
    user     = models.ForeignKey('User', on_delete=models.CASCADE)


class Campaign(models.Model):
    campaign_name = models.CharField(max_length=100, default = 'default')
    site = models.ForeignKey('Site', on_delete = models.CASCADE)
    status   = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField('date created', default=timezone.now)

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    status   = models.PositiveIntegerField(default = 1)
    campaign = models.ForeignKey('Campaign', on_delete = models.CASCADE, default=0)
    site = models.ForeignKey('Site', on_delete = models.CASCADE,default=0)
    created_at = models.DateTimeField('date created', default=timezone.now)

class Option(models.Model):
    name = models.CharField(max_length=100, default="none")
    relate_id   = models.PositiveIntegerField(default = 1)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    status   = models.PositiveIntegerField(default = 1)
    


