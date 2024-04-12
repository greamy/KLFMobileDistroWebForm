from django.shortcuts import render
from http import HTTPStatus
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.db.utils import IntegrityError
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.QRCode import QRCode
from .Scripts.DiskUtility import DiskUtility
from .models import Location, Site, Submission, Field, Description, PasswordCode
import socket
import datetime
import os
import random
import string

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
	# utility = DiskUtility()
	# db_file_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
	# db_size = utility.get_file_size(db_file_path)
	# server_size = utility.get_disk_usage(settings.BASE_DIR)[2]
	# return render(request, "WebForm/admin.html", {"db_size": db_size[0], "db_units": db_size[1],
	# 											  "server_size": round(server_size[0]), "server_units": server_size[1]})
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
			PasswordCode.objects.all().delete()
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

	new_username = request.POST["username"]
	new_email = request.POST['email']

	try:
		if request.user.email != new_email:
			send_mail(
				subject="Alert: KL&F Mobile Distribution System Email Change",
				message="The email used for password recovery of the admin account has been changed.\n" +
						"The new email for the admin account is: " + new_email + "\n" +
						"If you were not aware of this change, change your password immediately.\n" +
						"This can be done via the 'edit profile' dropdown in the top right of the admin panel.",
				from_email=None,
				recipient_list=[request.user.email, new_email],
				fail_silently=True
			)

		if request.user.username != new_username:
			send_mail(
				subject="Alert: KL&F Mobile Distribution System Username Change",
				message="The username used for the admin account login has been changed.\n" +
						"The new username for the admin account is: " + new_username + "\n" +
						"If you were not aware of this change, please change your password immediately.\n" +
						"This can be done via the 'edit profile' dropdown in the top right of the admin panel.",
				from_email=None,
				recipient_list=[new_email],
				fail_silently=True
			)
	except ValueError:
		pass

	request.user.username = new_username
	request.user.email = new_email
	request.user.save()

	return HttpResponse("Successfully changed username and email")


def validate_password(password):
	special_chars = "!@#$%^&*-~`<>,./?\\|-=+"
	if len(password) < 8:
		return -1, "Password must have at least 8 characters!"
	elif not any(char.isupper() for char in password):
		return -1, "Password must have at least one uppercase letter!"
	elif not any(char.islower() for char in password):
		return -1, "Password must have at least one lowercase letter!"
	elif not any(char in special_chars for char in password):
		return -1, "Password must have at least one special character: " + special_chars
	else:
		return 0, ""


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

		validation = validate_password(new_password)
		if validation[0] == -1:
			return render(request, "WebForm/ChangePassword.html", {"error": validation[1]})

		request.user.set_password(new_password)
		request.user.save()
		return HttpResponseRedirect("/form/change-password-success/")

	else:
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)


def change_password_success(request):
	return render(request, "WebForm/ChangePasswordSuccess.html", {})


def forgot_password(request):
	if request.method == "GET":
		return render(request, "WebForm/ForgotPassword.html", {})
	if request.method == "POST":
		# User can input either email or username associated with the admin account.
		email_username = request.POST['EmailUsername']
		admin_users = User.objects.all()
		for user in admin_users:
			if user.email == email_username or user.username == email_username:
				code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
				print(code)

				new_code = PasswordCode(code=code, email=email_username)
				new_code.save()
				try:
					send_mail(
						subject="Forgot Password Request KL&F Mobile Distribution System",
						message="A forgot password request for the admin page was sent.\n" +
								"The code to reset your password is: " + code + ".\n" +
								"If you did not request this code, disregard this email.",
						from_email=None,
						recipient_list=[user.email],
						fail_silently=True
					)
				except ValueError:
					return render(request, "WebForm/ForgotPassword.html", {"error": "Email client not set up. " +
																					"Forgot password functionality disabled."})
		return render(request, "WebForm/ForgotPasswordCode.html", {})
	else:
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)


def forgot_password_code(request):
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	code_submitted = request.POST['Code']
	# Forgot password code times out after 30 minutes
	timeout = datetime.datetime.now() - datetime.timedelta(seconds=60 * 30)
	print(timeout)
	codes_db = PasswordCode.objects.filter(generation_time__gte=timeout)
	if codes_db.exists():
		code_db = codes_db.last()
		if code_submitted == code_db.code:
			return render(request, "WebForm/ForgotPasswordChange.html", {"email": code_db.email})

	return render(request, "WebForm/ForgotPasswordCode.html",
				  {"error": "Incorrect code. Check your spam folder for more recent codes."})


def forgot_password_reset(request):
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	new_password = request.POST["Password"]
	email = request.POST['Email']

	validation = validate_password(new_password)
	if validation[0] == -1:
		return render(request, "WebForm/ForgotPasswordChange.html", {"error": validation[1], "email": email})

	admin_users = User.objects.all()
	success = False
	for user in admin_users:
		if user.email == email:
			user.set_password(new_password)
			user.save()
			success = True
	if success:
		return HttpResponseRedirect("/form/change-password-success/")
	else:
		return render(request, "WebForm/ForgotPasswordChange.html", {"error": "Error Occurred. Please try again.",
																	 "email": email, "redirect": 1})


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
	template = loader.get_template('WebForm/Sindex.html')

	user_data = request.POST
	headers_db = Field.objects.all().values("field_id", "tefap", "visible")

	extra_fields = {}
	for header in headers_db:
		if not header['tefap'] and header['visible']:
			extra_fields[header['field_id']] = user_data.get(header['field_id'])

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

	excel_data = []
	for row in model_data:
		row = list(row.values())
		if type(row[-1]) == dict:
			extra = row.pop()
			for field in extra_fields:
				row.append(extra.get(field))
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


def delete_old_entries(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if request.method != "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
	old_submissions = Submission.objects.filter(date__lte=one_year_ago)
	if old_submissions.exists():
		old_submissions.delete()
	return HttpResponse("Successfully deleted entries over a year old!!")


def get_form_fields(request):
	if request.method != "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	return JsonResponse(load_fields_from_db(), safe=False)


def load_fields_from_db():
	fields = Field.objects.all()
	settings = []
	for field in fields:
		settings.append([field.field_id, field.placeholder, field.name, field.field_type, 1 if field.required else 0,
						 field.field_min, field.field_max, 1 if field.visible else 0, 1 if field.tefap else 0,
						 field.order_num])

	return sorted(settings, key=lambda x: x[-1])


# return JsonResponse(settings, safe=False)


def save_form_fields(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if request.method != "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	# post_data = request.POST["fieldData"]
	# new_description = request.POST["description"]
	post_data = request.POST.lists()

	for settings in post_data:
		if settings[0] == "description":
			continue
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

	Description.objects.all().update(description=request.POST['description'])
	return JsonResponse(load_fields_from_db(), safe=False)


def remove_form_field(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if not request.method == "POST":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	form_field = request.POST.get("field")
	field = Field.objects.filter(field_id__iexact=form_field)

	if field.exists():
		field.delete()
	else:
		return JsonResponse({'error': 'Field object not found in database'}, status=404)

	return JsonResponse(load_fields_from_db(), safe=False)


def get_description(request):
	if not request.user.is_authenticated:
		return JsonResponse(LOGIN_REDIRECT_JSON)
	if not request.method == "GET":
		return HttpResponseBadRequest(INVALID_REQUEST_TYPE)

	return JsonResponse(Description.objects.all().first().description, safe=False)
