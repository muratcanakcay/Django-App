from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    handle = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        
class  Zone(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) # keep the user in db when the zone is deleted
    topic  = models.ForeignKey(Topic, on_delete = models.SET_NULL, null=True) # keep the topic in db when the zone is deleted
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] #shows the newes gossip first 

    def __str__(self):
        return self.name

class Gossip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # delete the gossip when the user is deleted
    zone = models.ForeignKey(Zone, on_delete = models.CASCADE) # delete the gossip when the zone is deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] #shows the newes gossip first

    def __str__(self):
        return self.body[0:50]