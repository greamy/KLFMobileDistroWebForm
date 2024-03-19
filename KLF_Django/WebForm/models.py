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
	# create one column ("Extra Fields") that stores all of the custom fields added later on as json
	# later we'll parse in our views so that the data gets split into different columns when put into excel file


# Model (Field) for storing field information from form.js
# This will replace the hardcoded fields in form.js
# from tehn on we would need server requests to get the infromation fro each field
# so server requests




