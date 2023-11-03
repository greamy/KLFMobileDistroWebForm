from django.shortcuts import render
from django.http import HttpResponse	#HttpResponse is an object, we need to point this object to the form html file
from django.template import loader

def index(request):
	return render(request, "WebForm/index.html", {})


def admin(request):
	return render(request, "WebForm/admin.html", {})


def submit(request):
	if request.method == "POST":
		template = loader.get_template('WebForm/Sindex.html')
		print("First Name = " + str(request.POST['Fname']))
		print("Last Name = " + str(request.POST.get("Lname")))
		print("Email = " + str(request.POST.get("Email")))
		return HttpResponse(template.render({}, request))
	else:
		return HttpResponse("Howd you do dat?")

#create functions, urls,py calls these functions to handle urls like /admin, /about, etc
#this will generate responses from thes functions, for instance, calling the html file for the user form. 

# Create your views here.
