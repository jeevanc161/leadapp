from django.db import models
from django.db.models.fields import EmailField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_organisation = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey('Agent', blank=True , null=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    category = models.ForeignKey('category' , related_name='leads' ,null=True , blank=True  , on_delete=models.SET_NULL)
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Agent(models.Model):
    user = models.OneToOneField('User', on_delete= models.CASCADE)
    organisation = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30) # New, Contected ,  Converted , Unconverted
    organisation = models.ForeignKey(UserProfile , on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Contactus(models.Model):

    name  = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



def post_user_created_signal(sender , instance , created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
     

post_save.connect(post_user_created_signal, sender= User)


