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


#class Submission
# we need a table with columns for first name last name etc, 
# but we also need the date submitted
# and the site submitted from (in url currently) that is linked to site database through a foreign key "Site" from the location/site databases above



