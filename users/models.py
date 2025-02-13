import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profiles/',default='profiles/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str( self.user.username )
    
class Message(models.Model):
        sender = models.ForeignKey(
            Profile, on_delete=models.SET_NULL, null=True, blank=True)
        recipient = models.ForeignKey(
            Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
        name = models.CharField(max_length=200, null=True, blank=True)
        email = models.EmailField(max_length=200, null=True, blank=True)
        subject = models.CharField(max_length=200, null=True, blank=True)
        body = models.TextField()
        is_read = models.BooleanField(default=False, null=True)
        created = models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True,
                            primary_key=True, editable=False)

        def __str__(self):
            return self.subject

        class Meta:
            ordering = ['is_read', '-created']

    
