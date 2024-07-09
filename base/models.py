from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE



class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # when room is deleted the topic can have reference to other rooms so we do not 
    # delete it but we set it to null on_delete thus null= True allows us to store null
    # value for topic in database
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # null is to allow it in database 
    # blank is in the form so the user can enter the field later so it can be left behind
    
    participants = models.ManyToManyField(User, related_name='participents', blank=True)
    updated = models.DateTimeField(auto_now=True)
    # saves when saved everytime
    created = models.DateTimeField(auto_now_add=True)
    # saves when its saved the initial/first time only

    def __str__(self):
        return self.name
    class Meta: 
        ordering = ['-updated', '-created']
    
class Message(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # room and massage are in one to many relation therefore when room is deleted 
    # on_delete = models.cascade will delete the corresponding messages 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    
    class Meta: 
        ordering = ['-updated', '-created']