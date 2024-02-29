from django.test import TestCase, Client
from django.http import JsonResponse
from django.db import transaction
from .models import Site, Location, Submission


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
		self.submission_dict = {"Fname": self.Fname, "Lname":self.Lname, "Email": self.Email, 
						"HHold": self.HHold, "Address":self.Address, "Zip": self.Zip}

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













