from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.TextField()

class Site(models.Model):
    name = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
