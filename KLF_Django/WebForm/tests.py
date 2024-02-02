from django.test import TestCase
from django.test import Client
from django.http import JsonResponse

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
	def test_get_locations(self):
		response = self.client.get("/form/get-location-data/")
		self.assertEqual(response.status_code, 200)
		self.assertIsInstance(response, JsonResponse)
	def test_add_location(self):
		response = self.client.post("/form/post-location-data/", {"newLocation": "TestLocation", "newSite": "TestSite"})
		self.assertContains(response, "TestLocation")
	def test_remove_location(self):
		response = self.client.post("/form/delete-location-data/", {"location": "TestLocation", "site": "TestSite"})
		self.assertNotContains(response, "TestLocation")









