from django.shortcuts import render
from django.http import HttpResponse	#HttpResponse is an object, we need to point this object to the form html file
from django.template import loader
from .Scripts.ExcelHandler import ExcelFile





def index(request):
	return render(request, "WebForm/index.html", {})


def admin(request):
	return render(request, "WebForm/admin.html", {})


def submit(request):
	if request.method == "POST":
		
		#folder_path = "/WebForm/ExcelDocs/"	#Ben added this 11/10
		#file_path = folder_path + "MobileFoodDistro.xlsx"	#Ben added this 11/10
		

		template = loader.get_template('WebForm/Sindex.html')
		user_data = [request.POST.get("Fname"), 
					 request.POST.get("Lname"), 
					 request.POST.get("Email"), 
					 request.POST.get("HHold"), 
					 request.POST.get("Address"), 
					 request.POST.get("Zip")
					]
		headers = ["First Name", "Last Name", "Email", "# in House", "Address", "Zip"]
		datafile = ExcelFile("MobileFoodDistro.xlsx", headers)	#Ben added changed this 11/10
		datafile.addData(user_data)		
		datafile.saveFile()
		return HttpResponse(template.render({}, request))
	else:
		return HttpResponse("Howd you do dat?")

#create functions, urls,py calls these functions to handle urls like /admin, /about, etc
#this will generate responses from thes functions, for instance, calling the html file for the user form. 

# Create your views here.
