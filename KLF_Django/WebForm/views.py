from django.shortcuts import render
from django.http import HttpResponse	#HttpResponse is an object, we need to point this object to the form html file
from django.template import loader
from .Scripts.ExcelHandler import ExcelFile
from .Scripts.QRCode import QRCode




def index(request):
	return render(request, "WebForm/index.html", {})


def admin(request):
	return render(request, "WebForm/admin.html", {})

def GenerateQR(request):
	QR = QRCode("data")
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
		datafile = ExcelFile("MobileFoodDistro.xlsx", headers, "WebForm/ExcelDocs")	#Hardcoded reference for now, this will end up being split between the different locations so they save in different folders. 
		datafile.addData(user_data)		
		datafile.saveFile()
		return HttpResponse(template.render({}, request))
	else:
		return HttpResponse("Howd you do dat?")

#create functions, urls,py calls these functions to handle urls like /admin, /about, etc
#this will generate responses from thes functions, for instance, calling the html file for the user form. 

# Create your views here.
