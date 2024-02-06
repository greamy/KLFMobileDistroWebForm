from django.test import TestCase, Client
from django.http import JsonResponse
from django.db import transaction
from .models import Site, Location


# Test simple pages to check if get requets are valid
class BasicPagesTestCase(TestCase):

	def test_form_page(self):
		c = Client()
		response = c.get("/form/")

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

	def test_add_location(self):
		# Action:
		# 	Add test site
		# Tests:
		#	Response contains added site
		# 	Database contains the new row
		response = self.client.post("/form/post-location-data/",
									{"newLocation": self.test_loc_name, "newSite": self.test_site_names[0]})
		self.assertContains(response, "TestLocation")
		self.assertTrue(Site.objects.filter(name__iexact=self.test_site_names[0]).exists())

		# Action:
		# 	Add duplicate test site
		# Tests:
		#	Database does not contain duplicate data (ie. add site request did not create duplicate row)
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
