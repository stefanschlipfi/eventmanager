from django.db import models,DataError
from django.contrib.auth.models import User
#from phone_field import PhoneField

class Event(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(default='event-images/default.png', upload_to='event-images')
    descripton = models.TextField(null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)
    #members = models.ManyToManyField(EventUser)

    def get_members(self):
        return EventUser.objects.filter(event=self.id)

    def __str__(self):
        return self.name

class EventUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ACTION_CHOICES = [
        ('accept','Teilnehmen'),
        ('maybe','Mit Vorbehalt'),
        ('reject','Absagen')
    ]
    action = models.CharField(max_length=6,choices=ACTION_CHOICES)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    comment = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} {self.action} {self.event.name}'

    def save(self,*args,**kwargs):
        all_user_objects = EventUser.objects.filter(user=self.user)
        pk_exits = all_user_objects.filter(pk=self.pk)

        #dont allow to create duplicate of EventUser
        if len(all_user_objects.filter(event = self.event)) > 0 and len(pk_exits) == 0:
            raise DataError("EventUser: {} allready exists in event: {}".format(self.user.username,self.event.name))
        super().save(*args,**kwargs)

# Create your models here.


class UserProps(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    age = models.IntegerField(blank=True,null=True)
#    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        if self.user.get_full_name() == "": 
            return f'{self.user.username}'
        return f'{self.user.get_full_name()}'