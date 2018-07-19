from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return '>>%s: < %s >' % (self.id, self.email)


class Site(models.Model):
    site_name = models.CharField(max_length=100, default="default")
    site_token = models.CharField(max_length=150, default=uuid.uuid4().hex)
    site_url = models.CharField(max_length=100)
    site_type = models.CharField(max_length=100, default="default")
    status = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField('date created', default=timezone.now)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return '>>%s: < %s >' % (self.id, self.site_name)

class widget_customization(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    sitename = models.ForeignKey('Site', on_delete=models.CASCADE)
    widget_color = models.CharField(max_length=100)
    widget_background = models.CharField(max_length=100)
    widget_outer_ring_color = models.CharField(max_length=100)

    def __str__(self):
        return '>>%s: < %s >' % (self.id, self.sitename, self.widget_color, self.widget_background, self.widget_outer_ring_color )



class Campaign(models.Model):
    campaign_name = models.CharField(max_length=100, default='default')
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    hits_count = models.PositiveIntegerField(default=0)
    unique_hits = models.PositiveIntegerField(default=0)
    subscriber_count = models.PositiveIntegerField(default=0)
    conversion = models.CharField(max_length=10, default="0")
    status = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return '>>%s: < %s >' % (self.id, self.campaign_name)


class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    status = models.PositiveIntegerField(default=1)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, default=0)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, default=0)
    created_at = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return '>>%s: < %s >' % (self.id, self.email)


class Option(models.Model):
    name = models.CharField(max_length=100, default="none")
    relate_id = models.PositiveIntegerField(default=1)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    status = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '>>%s: < %s >' % (self.id, self.key)


class Analytics(models.Model):
    created_at = models.DateTimeField('date created', default=timezone.now)
    cookie = models.CharField(max_length=100)
    site_token = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100)
    ip = models.CharField(max_length=50, default='0.0.0.0')


class ActiveUsers(models.Model):
    connected_at = models.DateTimeField('date connected', default=timezone.now)
    gone_at = models.DateTimeField('date gone', default=timezone.now)
    status = models.PositiveIntegerField(default=1)
    cookie = models.CharField(max_length=100)
    site_token = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100)
    ip = models.CharField(max_length=50, default='0.0.0.0')

    


