from django.contrib import admin
from .models import User, Site, Compaign, Subscriber

admin.site.register(User)
admin.site.register(Site)
admin.site.register(Compaign)
admin.site.register(Subscriber)


# Register your models here.
