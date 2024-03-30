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
	extra_fields = models.JSONField(default=dict)
	# create one column ("Extra Fields") that stores all of the custom fields added later on as json
	# later we'll parse in our views so that the data gets split into different columns when put into excel file


class Field(models.Model):
	type_choices = [("TXT", "text"), ("NUM", "number"), ("EML", "email"), ("OTH", "other")]
	
	field_id = models.TextField()
	placeholder = models.TextField()
	name = models.TextField()
	field_type = models.CharField(choices=type_choices, max_length=3)
	required = models.BooleanField()
	field_min = models.IntegerField(null=True, blank=True)
	field_max = models.IntegerField(null=True, blank=True)
	visible = models.BooleanField()
	tefap = models.BooleanField()
	order_num = models.IntegerField()


# Model (Field) for storing field information from form.js
# This will replace the hardcoded fields in form.js
# from tehn on we would need server requests to get the infromation fro each field
# so server requests




