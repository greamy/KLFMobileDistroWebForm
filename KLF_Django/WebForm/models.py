from django.db import models
from django.db.models.functions import Lower

# Create your models here.
class Location(models.Model):
    name = models.TextField()

class Site(models.Model):
    name = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), "location", name="unique_name_location")
        ]
