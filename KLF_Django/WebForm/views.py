from django.shortcuts import render
from django.http import HttpResponse  # HttpResponse is an object, we need to point this object to the form html file
from django.http import JsonResponse
from django.template import loader
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.JsonHandler import JsonHandler
from .Scripts.QRCode import QRCode
from .models import Location, Site


def index(request):
	return render(request, "WebForm/index.html", {})


def admin(request):
	return render(request, "WebForm/admin.html", {})


def generate_QR(request):
	QR = QRCode("google.com")
	QR.saveImage("WebForm/QR_Codes/QR.png")
	return HttpResponse("test")


def submit(request):
	if request.method == "POST":
		template = loader.get_template('WebForm/Sindex.html')
		user_data = [request.POST.get("Fname"),
					request.POST.get("Lname"),
					request.POST.get("Email"),
					request.POST.get("HHold"),
					request.POST.get("Address"),
					request.POST.get("Zip")
					]
		headers = ["First Name", "Last Name", "Email", "# in House", "Address", "Zip"]
		# TODO: Dynamically update file path based on location
		datafile = ExcelFile("MobileFoodDistro.xlsx", headers, "WebForm/ExcelDocs")
		datafile.addData(user_data)
		datafile.saveFile()
		return HttpResponse(template.render({}, request))
	else:
		return HttpResponse("Howd you do dat?")


# create functions, urls,py calls these functions to handle urls like /admin, /about, etc
# this will generate responses from these functions, for instance, calling the html file for the user form.

def get_locations(request):
	file_path = 'WebForm/locations.json'
	try:
		handler = JsonHandler(file_path)
		locations = handler.get_data()

		return JsonResponse(locations, safe=False)
	except FileNotFoundError:
		return JsonResponse({'error': 'Locations JSON file not found'}, status=404)


def create_site(request):
	file_path = 'WebForm/locations.json'
	loc_name = request.POST.get("newLocation")
	site_name = request.POST.get("newSite")
	loc_dict = {loc_name: [site_name]}

	loc = Location.objects.filter(name__iexact=loc_name)
	if loc.exists():
		site = Site(name=site_name, location=loc)
		site.save()
	else:
		loc = Location(name=loc_name)
		loc.save()
		site = Site(name=site_name, location=loc)
		site.save()


	try:
		handler = JsonHandler(file_path)
		handler.add_data(loc_dict)
		handler.save_json(file_path)
		return JsonResponse(handler.get_data(), safe=False)
	except FileNotFoundError:
		return JsonResponse({'error': 'Locations JSON file not found'}, status=404)


def delete_site(request):
	file_path = 'WebForm/locations.json'
	loc = request.POST.get("location")
	site = request.POST.get("site")
	try:
		handler = JsonHandler(file_path)
		handler.remove_data(loc, site)
		handler.save_json(file_path)
		return JsonResponse(handler.get_data(), safe=False)
	except FileNotFoundError:
		return JsonResponse({'error': 'Locations JSON file not found'}, status=404)
