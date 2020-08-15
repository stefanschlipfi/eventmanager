from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProps


@receiver(post_save, sender=User)
def create_userprops(sender,instance, created, **kwargs):
    if created:
        UserProps.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_userprops(sender,instance, **kwargs):
    instance.userprops.save()