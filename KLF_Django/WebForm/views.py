from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.utils import IntegrityError
from django.template import loader
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.JsonHandler import JsonHandler
from .Scripts.QRCode import QRCode
from .models import Location, Site, Submission


# create functions, urls,py calls these functions to handle urls like /admin, /about, etc
# this will generate responses from these functions, for instance, calling the html file for the user form.

def index(request, site):
	return render(request, "WebForm/index.html", {})


def admin(request):
	return render(request, "WebForm/admin.html", {})


def generate_QR(request):
	print(request.GET)
	location = request.GET.get("location")
	site = request.GET.get("site")
	#QR = QRCode(location + " : " + site)
	QR = QRCode("192.168.40.159:8000/form/" + site)

	QR.saveImage("WebForm/QR_Codes/QR.png")
	with open("WebForm/QR_Codes/QR.png", 'rb') as img:
		response = HttpResponse(img.read(), content_type="image/png")
		response["Content-Disposition"] = 'attachment; filename="QR.png"'
	return response





def submit(request, site_name):
	print(site_name)
	

	if request.method == "POST":
		template = loader.get_template('WebForm/Sindex.html')
		user_data = [request.POST.get("Fname"),
					 request.POST.get("Lname"),
					 request.POST.get("Email"),
					 request.POST.get("HHold"),
					 request.POST.get("Address"),
					 request.POST.get("Zip")
					 ]
		
		site = Site.objects.filter(name__iexact=site_name)
		if site.exists():
			submission = Submission(first_name=user_data[0], last_name=user_data[1], email=user_data[2], 
						number_in_household=user_data[3], street_address=user_data[4], zip_code=user_data[5], site=site.first())

			submission.save()
		else:
			return HttpResponse("Invalid Site Name")

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
	try:
		if loc.exists():
			site = Site(name=site_name, location=loc.first())
			site.save()
		else:
			loc = Location(name=loc_name)
			loc.save()
			site = Site(name=site_name, location=loc)
			site.save()
	except IntegrityError:
		return HttpResponseBadRequest('Site already exists at that location.')
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


