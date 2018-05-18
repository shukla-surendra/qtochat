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


class Compaign(models.Model):
    compaign_name = models.CharField(max_length=100)
    site = models.ForeignKey('Site', on_delete = models.CASCADE)
    created_at = models.DateTimeField('date created', default=timezone.now)

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField('date created', default=timezone.now)


