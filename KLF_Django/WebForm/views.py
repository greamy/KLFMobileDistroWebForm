from django.shortcuts import render
from django.http import HttpResponse  # HttpResponse is an object, we need to point this object to the form html file
from django.http import JsonResponse
from django.template import loader
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.JsonHandler import JsonHandler
from .Scripts.QRCode import QRCode
from .models import Location, Site

# create functions, urls,py calls these functions to handle urls like /admin, /about, etc
# this will generate responses from these functions, for instance, calling the html file for the user form.

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

def get_locations(request):
	sites = Site.objects.all()
	site_dict = {}
	for site in sites:
		if site.location.name in site_dict:
			site_dict[site.location.name].append(site.name)
		else:
			site_dict[site.location.name] = [site.name]

	return JsonResponse(site_dict, safe=False)

def create_site(request):
	loc_name = request.POST.get("newLocation")
	site_name = request.POST.get("newSite")

	loc = Location.objects.filter(name__iexact=loc_name)

	if loc.exists():
		site = Site(name=site_name, location=loc.first())
		site.save()
	else:
		loc = Location(name=loc_name)
		loc.save()
		site = Site(name=site_name, location=loc)
		site.save()

	return get_locations(request)

def delete_site(request):
	loc_name = request.POST.get("location")
	site_name = request.POST.get("site")

	site = Site.objects.filter(name__iexact=site_name)
	if site.exists():
		site.delete()
		other_sites = Site.objects.filter(location__name__iexact=loc_name)
		if not other_sites.exists():
			Location.objects.filter(name__iexact=loc_name).delete()
	else:
		return JsonResponse({'error': 'Site object not found in database'}, status=404)

	return get_locations(request)






