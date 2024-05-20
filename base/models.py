from django.db import models
from django.contrib.auth.models import AbstractUser

# Define your custom User model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    pass



# Define the Topic model
class Topic(models.Model):
    name = models.CharField(max_length=100)
    scraped_data = models.TextField(blank=True)
    summary = models.TextField(blank=True) 
    filename = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Topic:{self.name}"