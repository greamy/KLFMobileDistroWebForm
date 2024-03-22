from django.shortcuts import render
from http import HTTPStatus
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.db.utils import IntegrityError
from django.template import loader
from django.conf import settings
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.QRCode import QRCode
from .models import Location, Site, Submission
import socket
import datetime
import os


# create functions, urls,py calls these functions to handle urls like /admin, /about, etc
# this will generate responses from these functions, for instance, calling the html file for the user form.
ADMIN_HOME_URL = "/form/admin/"
LOGIN_REDIRECT_URL = ADMIN_HOME_URL + "login/"
LOGIN_REDIRECT_JSON = {"redirect": LOGIN_REDIRECT_URL}
APPLICATION_DIR = os.path.join(settings.BASE_DIR, "WebForm")
INVALID_REQUEST_TYPE = "Invalid Request type."

class HttpResponseUnauthorized(HttpResponse):
	status_code = HTTPStatus.UNAUTHORIZED

def index(request, site):
	return render(request, "Webform/index.html", {})

@login_required
def admin(request):
	return render(request, "WebForm/admin.html", {})

def admin_login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(ADMIN_HOME_URL)

	if request.method == "GET":
		return render(request, "WebForm/LoginIndex.html", {})
	elif request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return JsonResponse(LOGIN_REDIRECT_JSON)
		else:
			return HttpResponseUnauthorized("Username or Password was Incorrect. Please Try Again.")
	else:
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)


def logout_user(request):
	if request.user.is_authenticated:
		logout(request)
	return JsonResponse(LOGIN_REDIRECT_JSON)

def change_username(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(LOGIN_REDIRECT_URL)
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	new_username = request.POST["Username"]
	request.user.username = new_username
	return HttpResponse("Successfully changed username")

def change_password(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(LOGIN_REDIRECT_URL)
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	new_password = request.POST["Password"]
	request.user.set_password(new_password)
	return HttpResponse("Successfully changed password")


def generate_QR(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if request.method != "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	location = request.GET.get("location")
	site = request.GET.get("site")
	cur_ip = socket.gethostbyname(socket.gethostname())
	QR = QRCode("http://" + cur_ip + "/form/" + site + "/")

	file_name = "QR.png"
	path = os.path.join(APPLICATION_DIR, "QR_CODES", file_name)
	QR.saveImage(path)
	with open(path, 'rb') as img:
		response = HttpResponse(img.read(), content_type="image/png")
		response["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
	return response


def submit(request, site_name):
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	template = loader.get_template('WebForm/Sindex.html')
	user_data = [request.POST.get("Fname"),
				 request.POST.get("Lname"),
				 request.POST.get("Email"),
				 request.POST.get("HHold"),
				 request.POST.get("Address"),
				 request.POST.get("Zip")
				 ]

	# input validation
	if '@' not in user_data[2] or '.' not in user_data[2]:
		return HttpResponseBadRequest("Invalid Email Address")
	try:
		hhold = int(user_data[3])
	except ValueError:
		return HttpResponseBadRequest("Invalid Number in Household")

	site = Site.objects.filter(name__iexact=site_name)
	if not site.exists():
		return HttpResponseBadRequest("Invalid Site Name in URL.")

	submission = Submission(first_name=user_data[0], last_name=user_data[1], email=user_data[2],
							number_in_household=user_data[3], street_address=user_data[4],
							zip_code=user_data[5], site=site.first())

	submission.save()

	return HttpResponse(template.render({}, request))


def get_locations(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)

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
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if not request.method == "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

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
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if not request.method == "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

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
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if request.method != "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

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
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if request.method != "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

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
	directory = os.path.join(APPLICATION_DIR, "ExcelDocs")
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
