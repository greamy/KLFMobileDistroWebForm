from django.shortcuts import render
from http import HTTPStatus
from time import sleep
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.db.utils import IntegrityError
from django.template import loader
from django.conf import settings
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.QRCode import QRCode
from .models import Location, Site, Submission, Field
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
	if request.method == "GET":
		return render(request, "WebForm/index.html", {})
	elif request.method == "POST":
		return submit(request, site)


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

def get_profile_info(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(LOGIN_REDIRECT_URL)
	if request.method != "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	username = request.user.username
	email = request.user.email

	return JsonResponse({"username": username, "email": email}, safe=False)


def change_username(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(LOGIN_REDIRECT_URL)
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	print(request.user)

	new_username = request.POST["username"]
	new_email = request.POST['email']
	print(new_username, new_email)
	request.user.username = new_username
	request.user.email = new_email
	request.user.save()

	print(request.user.email)

	return HttpResponse("Successfully changed username and email")


def change_password(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(LOGIN_REDIRECT_URL)
	if request.method == "GET":
		return render(request, "WebForm/ChangePassword.html", {})

	elif request.method == "POST":
		cur_password = request.POST["CurrentPassword"]
		user = authenticate(request, username=request.user.username, password=cur_password)
		if user is None:
			return render(request, "WebForm/ChangePassword.html", {"error": "Current Password is incorrect"})

		new_password = request.POST["Password"]
		request.user.set_password(new_password)
		return HttpResponseRedirect("/form/change-password-success/")
	
	else:
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)
	

def change_password_success(request):
	return render(request, "WebForm/ChangePasswordSuccess.html", {})


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
	path = os.path.join(APPLICATION_DIR, "QR_Codes", file_name)
	QR.saveImage(path)
	with open(path, 'rb') as img:
		response = HttpResponse(img.read(), content_type="image/png")
		response["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
	return response


def submit(request, site_name):
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)
	print(request.POST)
	template = loader.get_template('WebForm/Sindex.html')

	user_data = request.POST
	headers_db = Field.objects.all().values("field_id", "tefap", "visible")

	extra_fields = {}
	for header in headers_db:
		if not header['tefap'] and header['visible']:
			extra_fields[header['field_id']] = user_data.get(header['field_id'])

	print(extra_fields)

	# input validation
	if '@' not in user_data['Email'] or '.' not in user_data['Email']:
		template = loader.get_template('WebForm/index.html')
		return HttpResponse(
			template.render({"error": "Invalid Email address. Must include '@' and '.' characters."}, request))
	try:
		int(user_data['HHold'])
	except ValueError:
		template = loader.get_template('WebForm/index.html')
		return HttpResponse(
			template.render({"error": "Invalid Email address. Must include '@' and '.' characters."}, request))

	site = Site.objects.filter(name__iexact=site_name)
	if not site.exists():
		return HttpResponseBadRequest("Invalid Site Name in URL.")

	submission = Submission(first_name=user_data['Fname'], last_name=user_data['Lname'], email=user_data['Email'],
							number_in_household=user_data['HHold'], street_address=user_data['Address'],
							zip_code=user_data['Zip'], site=site.first(), extra_fields=extra_fields)

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

# TODO Get headers from Fields Database
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
				Zip_Code=F("zip_code"), Site_Name=F("site__name"), Date=F("date"), Extra_Fields=F("extra_fields"))

	headers_db = Field.objects.all().values("field_id", "tefap")
	headers = []
	extra_fields = []
	for header in headers_db:
		if header['tefap']:
			headers.append(header['field_id'])
		else:
			extra_fields.append(header['field_id'])
	headers.append("Site Name")
	headers.append("Date")
	headers.extend(extra_fields)

	# print(headers)
	excel_data = []
	for row in model_data:
		row = list(row.values())
		if type(row[-1]) == dict:
			extra = row.pop()
			for field in extra_fields:
				row.append(extra.get(field))
		print(row)
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


def get_form_fields(request):
	if request.method != "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	return load_fields_from_db()


def load_fields_from_db():
	fields = Field.objects.all()
	settings = []
	for field in fields:
		settings.append([field.field_id, field.placeholder, field.name, field.field_type, 1 if field.required else 0,
						 field.field_min, field.field_max, 1 if field.visible else 0, 1 if field.tefap else 0,
						 field.order_num])
	return JsonResponse(settings, safe=False)


def save_form_fields(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	post_data = request.POST.lists()

	for settings in post_data:
		settings = settings[1]

		updated = Field.objects.filter(field_id__iexact=settings[0]) \
			.update(placeholder=settings[1], field_type=settings[2], required=True if settings[3] == "true" else False,
					field_min=None if settings[4] == "" else settings[4],
					field_max=None if settings[5] == "" else settings[5],
					visible=True if settings[6] == "true" else False,
					order_num=int(settings[7]))

		if updated == 0:
			new_field = Field(field_id=settings[0], placeholder=settings[1], name=settings[0], field_type=settings[2],
							required=True if settings[3] == "true" else False,
							field_min=None if settings[4] == "" else settings[4],
							field_max=None if settings[5] == "" else settings[5],
							visible=True if settings[6] == "true" else False,
							tefap=False,
							order_num=int(settings[7]))
			new_field.save()

	return load_fields_from_db()


def remove_form_field(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if not request.method == "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	form_field = request.POST.get("field")
	print(form_field)
	field = Field.objects.filter(field_id__iexact=form_field)

	if field.exists():
		field.delete()
	else:
		return JsonResponse({'error': 'Field object not found in database'}, status=404)

	return load_fields_from_db()












