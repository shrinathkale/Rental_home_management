from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    rooms = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="property_images/")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
