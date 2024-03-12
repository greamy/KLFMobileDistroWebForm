from django.test import TestCase, Client
from django.http import JsonResponse
from django.db import transaction
from .models import Site, Location, Submission
import datetime
import json


# Test simple pages to check if get requets are valid
class BasicPagesTestCase(TestCase):

	def test_form_page(self):
		c = Client()
		response = c.get("/form/test/")
		self.assertContains(response, '<form method="POST"', status_code=200, html=False)

	def test_admin_page(self):
		c = Client()
		response = c.get("/form/admin/")
		self.assertContains(response, '<form action="javascript:', status_code=200, html=False)


class LocationActionTestCases(TestCase):
	def setUp(self):
		self.client = Client()
		self.test_loc_name = "TestLocation"
		self.test_site_names = ["TestSite1", "TestSite2"]

	def test_get_locations(self):
		response = self.client.get("/form/get-location-data/")
		self.assertEqual(response.status_code, 200)
		self.assertIsInstance(response, JsonResponse)

	def test_add_site(self):
		# Action:
		# 	Add test site
		# Tests:
		#	Response contains added site
		# 	Database contains the new row
		response = self.client.post("/form/post-location-data/",
									{"newLocation": self.test_loc_name, "newSite": self.test_site_names[0]})
		self.assertContains(response, "TestLocation")
		self.assertTrue(Site.objects.filter(name__iexact=self.test_site_names[0]).exists())

	def test_add_duplicate_site(self):
		# Action:
		# 	Add duplicate test site
		# Tests:
		#	Database does not contain duplicate data (ie. add site request did not create duplicate row)
		loc = Location(name=self.test_loc_name)
		loc.save()
		new_site = Site(name=self.test_site_names[0], location=loc)
		new_site.save()

		with transaction.atomic():
			response = self.client.post("/form/post-location-data/",
										{"newLocation": self.test_loc_name, "newSite": self.test_site_names[0]})
		self.assertContains(response, "Site already exists", status_code=400)
		self.assertEqual(Site.objects.filter(name__iexact=self.test_site_names[0]).count(), 1)

	def test_remove_location(self):
		# add rows to database to be able to remove
		loc = Location(name=self.test_loc_name)
		loc.save()
		site1 = Site(name=self.test_site_names[0], location=loc)
		site1.save()

		site2 = Site(name=self.test_site_names[1], location=loc)
		site2.save()

		# Action:
		# 	Remove the first site
		# Tests:
		#	Response does not contain removed site
		# 	Site (but not location) is removed from the database.
		response = self.client.post("/form/delete-location-data/",
									{"location": self.test_loc_name, "site": self.test_site_names[0]})
		self.assertNotContains(response, self.test_site_names[0])
		self.assertFalse(Site.objects.filter(name__iexact=self.test_site_names[0]).exists())
		self.assertTrue(Location.objects.filter(name__iexact=self.test_loc_name).exists())

		# Action:
		# 	Remove the second site,
		# Tests:
		#	Resopnse does not contain removed site
		# 	Site AND location are removed from the database.
		response = self.client.post("/form/delete-location-data/",
									{"location": self.test_loc_name, "site": self.test_site_names[1]})
		self.assertNotContains(response, self.test_site_names[1])
		self.assertFalse(Site.objects.filter(name__iexact=self.test_site_names[1]).exists())
		self.assertFalse(Location.objects.filter(name__iexact=self.test_loc_name).exists())


class SubmissionTestCases(TestCase):
	def setUp(self):
		self.client = Client()

		self.Fname = "test Fname"
		self.Lname = "test Lname"
		self.Email = "test Email"
		self.HHold = 1
		self.Address = "test Address"
		self.Zip = "12345"
		self.submission_dict = {"Fname": self.Fname, "Lname": self.Lname, "Email": self.Email,
								"HHold": self.HHold, "Address": self.Address, "Zip": self.Zip}

		self.loc_name = "test location"
		loc = Location(name=self.loc_name)
		loc.save()

		self.site_name = "test site"
		site = Site(name=self.site_name, location=loc)
		site.save()

	def test_sumbit_form(self):
		response = self.client.post("/form/" + self.site_name + "/submit/", self.submission_dict)
		self.assertContains(response, "Thank you for your submission!")
		self.assertTrue(Submission.objects.filter(first_name__iexact=self.Fname).exists())


class SubmissionTableTestCases(TestCase):
	def setUp(self):
		self.client = Client()

		self.loc_name = "test location"
		loc = Location(name=self.loc_name)
		loc.save()

		self.site_name = "test site"
		site = Site(name=self.site_name, location=loc)
		site.save()

		self.request_dict = {"location": self.loc_name, "site": self.site_name}

		self.decoy_site_name = "decoy site"
		decoy_site = Site(name=self.decoy_site_name, location=loc)
		decoy_site.save()

		# Create a number of submissions with differing dates under a test site
		self.Fname = "test Fname"
		self.Lname = "test Lname"
		self.Email = "test Email"
		self.HHold = 1
		self.Address = "test Address"
		self.Zip = "12345"
		self.submission_dict = {"Fname": self.Fname, "Lname": self.Lname, "Email": self.Email,
								"HHold": self.HHold, "Address": self.Address, "Zip": self.Zip}

		submission1 = Submission(first_name="today", last_name=self.Lname, email=self.Email,
								number_in_household=self.HHold, street_address=self.Address,
								zip_code=self.Zip, site=site)
		submission1.save()

		submission2 = Submission(first_name="lastweek", last_name=self.Lname, email=self.Email,
								number_in_household=self.HHold, street_address=self.Address,
								zip_code=self.Zip, site=site)
		submission2.save()

		submission3 = Submission(first_name="tendays", last_name=self.Lname, email=self.Email,
								number_in_household=self.HHold, street_address=self.Address,
								zip_code=self.Zip, site=site)
		submission3.save()

		# Create at least one submission under another test site (to ensure proper filtering)

		submission_decoy = Submission(first_name="fivedays", last_name=self.Lname, email=self.Email,
								number_in_household=self.HHold, street_address=self.Address,
								zip_code=self.Zip, site=decoy_site)
		submission_decoy.save()

		# Update dates to have multiple submission dates
		self.lastweek = datetime.date.today() - datetime.timedelta(days=7)
		self.tendays = datetime.date.today() - datetime.timedelta(days=10)
		self.fivedays = datetime.date.today() - datetime.timedelta(days=5)

		Submission.objects.filter(first_name__iexact="lastweek").update(date=self.lastweek)
		Submission.objects.filter(first_name__iexact="tendays").update(date=self.tendays)
		Submission.objects.filter(site__name__iexact=self.decoy_site_name).update(date=self.fivedays)

	def test_load_submission_table(self):
		# Create a request to URL which will call views.get_submission_table
		# Check that returned value contains: [today, lastweek, tendays], and does not contain fivedays date.
		response = self.client.get("/form/get-submission-table/", data=self.request_dict)
		expected = {datetime.date.today(), self.lastweek, self.tendays}

		self.assertContains(response, list(expected)[0])

		returned_dates = json.loads(response.content.decode())
		for i, date in enumerate(returned_dates):
			returned_dates[i] = datetime.datetime.strptime(date, '%Y-%m-%d').date()
		returned_dates = set(returned_dates)
		self.assertSetEqual(returned_dates, expected)
