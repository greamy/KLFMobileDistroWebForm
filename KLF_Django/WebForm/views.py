from django.shortcuts import render
from django.http import HttpResponse	#HttpResponse is an object, we need to point this object to the form html file
from django.template import loader
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.QRCode import QRCode
import json
from django.http import JsonResponse


def index(request):
	return render(request, "WebForm/index.html", {})

def admin(request):
	return render(request, "WebForm/admin.html", {})

def GenerateQR(request):
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

#create functions, urls,py calls these functions to handle urls like /admin, /about, etc
#this will generate responses from these functions, for instance, calling the html file for the user form.

def getLocations(request):
	file_path = 'WebForm/locations.json'
	try:
		with open(file_path, 'r') as json_file:
			locations = json.load(json_file)
			print(locations)

		return JsonResponse(locations, safe=False)
	except FileNotFoundError:
		return JsonResponse({'error': 'CSV file not found'}, status=404)


