from django.contrib import admin
from .models import User, Site, Campaign, Subscriber, Option

admin.site.register(User)
admin.site.register(Site)
admin.site.register(Campaign)
admin.site.register(Subscriber)
admin.site.register(Option)



# Register your models here.
