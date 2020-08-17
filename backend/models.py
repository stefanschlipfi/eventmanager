from django.db import models
from django.contrib.auth.models import User
#from phone_field import PhoneField

class Event(models.Model):
    name = models.CharField(max_length=20)
    #members = models.ManyToManyField(EventUser)

    def get_members(self):
        return EventUser.objects.filter(event=self.id)

    def __str__(self):
        return self.name

class EventUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ACTION_CHOICES = [
        ('accept','Teilnehmen'),
        ('maybe','Mit vorbehalt'),
        ('reject','Absagen')
    ]
    action = models.CharField(max_length=6,choices=ACTION_CHOICES)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} {self.action} {self.event.name}'


  

# Create your models here.


class UserProps(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    age = models.IntegerField(blank=True,null=True)
#    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        if self.user.get_full_name() == "": 
            return f'{self.user.username}'
        return f'{self.user.get_full_name()}'