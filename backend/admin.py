from django.contrib import admin
from .models import UserProps,Event,EventUser
# Register your models here.
admin.site.register(UserProps)
admin.site.register(Event)
admin.site.register(EventUser)