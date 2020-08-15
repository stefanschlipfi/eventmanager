from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=20)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class UserProps(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    age = models.IntegerField(blank=True,null=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        if self.user.get_full_name() == "": 
            return f'{self.user.username}'
        return f'{self.user.get_full_name()}'