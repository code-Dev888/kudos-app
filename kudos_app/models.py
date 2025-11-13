from django.db import models
import uuid
from django.utils import timezone

class Organization(models.Model): #Represents the organization where the user belongs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    kudos_left = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.username} ({self.organization.name})"
    
class Kudo(models.Model): #For single kudo given by 1 user to other
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name="sent_kudos", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_kudos", on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.sender == self.receiver: #preventing from sending kudos to self
            raise ValueError("User cannot sent kudos to themselves.")
        
        if self.sender.kudos_left <= 0: #check if user has kudos to give
            raise ValueError(f"{self.sender.username} has no kudos left to give.")
        
        self.sender.kudos_left -= 1
        self.sender.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"




