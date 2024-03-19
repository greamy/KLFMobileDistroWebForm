from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.utils import IntegrityError
from django.template import loader
from django.conf import settings
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.JsonHandler import JsonHandler
from .Scripts.QRCode import QRCode
from .models import Location, Site, Submission
import socket
import datetime
import os


# create functions, urls,py calls these functions to handle urls like /admin, /about, etc
# this will generate responses from these functions, for instance, calling the html file for the user form.

def index(request, site):
	return render(request, "WebForm/index.html", {})


def admin(request):
	if request.user.is_authenticated:
		return render(request, "WebForm/admin.html", {})
	username = request.POST["Username"]
	password = request.POST["Password"]
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return render(request, "WebForm/admin.html", {})
	else:
		return render(request, "WebForm/LoginIndex.html", {})

def admin_login(request):
	if request.user.is_authenticated:
		return admin(request)
	return render(request, "WebForm/LoginIndex.html", {})

def logout_user(request):
	if not request.user.is_authenticated:
		return admin_login(request)
	logout(request)
	return admin_login(request)

def change_username(request):
	if not request.user.is_authenticated:
		return admin_login(request)
	new_username = request.POST["Username"]
	request.user.username = new_username
	return HttpResponse("Successfully changed username")

def change_password(request):
	if not request.user.is_authenticated:
		return admin_login(request)
	new_password = request.POST["Password"]
	request.user.set_password(new_password)
	return HttpResponse("Successfully changed password")

#def forgot_password


def generate_QR(request):
	if not request.user.is_authenticated:
		return admin_login(request)

	location = request.GET.get("location")
	site = request.GET.get("site")
	cur_ip = socket.gethostbyname(socket.gethostname())
	QR = QRCode("http://" + cur_ip + "/form/" + site + "/")

	QR.saveImage("WebForm/QR_Codes/QR.png")
	with open("WebForm/QR_Codes/QR.png", 'rb') as img:
		response = HttpResponse(img.read(), content_type="image/png")
		response["Content-Disposition"] = 'attachment; filename="QR.png"'
	return response


def submit(request, site_name):
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
									number_in_household=user_data[3], street_address=user_data[4],
									zip_code=user_data[5], site=site.first())

			submission.save()
		else:
			return HttpResponse("Invalid Site Name")

		return HttpResponse(template.render({}, request))
	else:
		return HttpResponse("Howd you do dat?")


def get_locations(request):
	if not request.user.is_authenticated:
		print(" not authenticated")
		return admin_login(request)
	sites = Site.objects.all()
	site_dict = {}
	for site in sites:
		if site.location.name in site_dict:
			site_dict[site.location.name].append(site.name)
		else:
			site_dict[site.location.name] = [site.name]

	return JsonResponse(site_dict, safe=False)


def create_site(request):
	if not request.user.is_authenticated:
		return admin_login(request)
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
	if not request.user.is_authenticated:
		return admin_login(request)
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


# Pull site and location string from request object
# Query Submission model for all submissions from site
# Figure out which days had at least one submission
# Return list-like object of days that had >= 1 submission
# {"02/10/24", "02/15/24", ...}
def get_submission_table(request):
	if not request.user.is_authenticated:
		return admin_login(request)
	location = request.GET.get("location")
	site = request.GET.get("site")

	unique_dates = list(Submission.objects.filter(site__name__iexact=site).dates("date", "day", "DESC"))

	return JsonResponse(unique_dates, safe=False)


def make_dummy_submissions(request):
	Fname = "test Fname"
	Lname = "test Lname"
	Email = "test Email"
	HHold = 1
	Address = "test Address"
	Zip = "12345"

	site = Site.objects.filter(name__iexact="Galesburg United Methodist Church").first()

	submission1 = Submission(first_name="today", last_name=Lname, email=Email,
							 number_in_household=HHold, street_address=Address,
							 zip_code=Zip, site=site)
	submission1.save()

	submission2 = Submission(first_name="1day", last_name=Lname, email=Email,
							 number_in_household=HHold, street_address=Address,
							 zip_code=Zip, site=site)
	submission2.save()

	submission3 = Submission(first_name="2day", last_name=Lname, email=Email,
							 number_in_household=HHold, street_address=Address,
							 zip_code=Zip, site=site)
	submission3.save()

	submission4 = Submission(first_name="3day", last_name=Lname, email=Email,
							 number_in_household=HHold, street_address=Address,
							 zip_code=Zip, site=site)
	submission4.save()

	submission5 = Submission(first_name="4day", last_name=Lname, email=Email,
							 number_in_household=HHold, street_address=Address,
							 zip_code=Zip, site=site)
	submission5.save()

	# Update dates to have multiple submission dates
	today = datetime.date.today()

	Submission.objects.filter(first_name__iexact="1day").update(date=today - datetime.timedelta(days=1))
	Submission.objects.filter(first_name__iexact="2day").update(date=today - datetime.timedelta(days=2))
	Submission.objects.filter(first_name__iexact="3day").update(date=today - datetime.timedelta(days=3))
	Submission.objects.filter(first_name__iexact="4day").update(date=today - datetime.timedelta(days=4))


def get_excel_file(request):
	if not request.user.is_authenticated:
		return admin_login(request)
	site = request.GET.get("site")
	date = request.GET.get("date")
	date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()

	model_data = Submission.objects \
		.filter(site__name__iexact=site) \
		.filter(date__exact=date_object) \
		.values(First_Name=F("first_name"), Last_Name=F("last_name"), Email=F("email"),
				Number_In_Household=F("number_in_household"), Street_Address=F("street_address"),
				Zip_Code=F("zip_code"), Site_Name=F("site__name"), Date=F("date"))

	excel_data = []
	headers = list(model_data.first().keys())

	for row in model_data:
		row = list(row.values())
		excel_data.append(row)

	file_name = site + " " + date + ".xlsx"
	directory = os.path.join(settings.BASE_DIR, "WebForm", "ExcelDocs")
	handler = ExcelFile(file_name, headers, directory)
	handler.add_data(excel_data)
	handler.save_file()

	excel_file = handler.get_file()
	response = HttpResponse(excel_file.read(),
							content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
	excel_file.close()
	handler.delete_file()

	return response
