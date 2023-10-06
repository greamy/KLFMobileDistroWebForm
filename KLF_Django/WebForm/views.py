from django.shortcuts import render
from django.http import HttpResponse	#HttpResponse is an object, we need to point this object to the form html file


def index(request):
	return render(request, "WebForm/index.html", {})


def admin(request):
	return render(request, "WebForm/admin.html", {})


#create functions, urls,py calls these functions to handle urls like /admin, /about, etc
#this will generate responses from thes functions, for instance, calling the html file for the user form. 

# Create your views here.
