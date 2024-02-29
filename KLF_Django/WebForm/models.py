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


class Submission(models.Model):
	first_name = models.TextField()
	last_name = models.TextField()
	email = models.TextField()
	number_in_household = models.IntegerField()
	street_address = models.TextField()
	zip_code = models.TextField()
	site = models.ForeignKey(Site, on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)
	




