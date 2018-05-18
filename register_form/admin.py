from django.contrib import admin
from .models import User, Site, Campaign, Subscriber

admin.site.register(User)
admin.site.register(Site)
admin.site.register(Campaign)
admin.site.register(Subscriber)


# Register your models here.
