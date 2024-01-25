"""
URL configuration for KLFMobile project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),		#path(route, view)
	path('get-location-data/', views.getLocations, name = 'getLocations'),
	path('post-location-data/', views.postLocations, name = 'postLocations'),
    path('admin/', views.admin, name = 'admin'),
	path('submit/', views.submit, name = 'submit'),
	path('QR/', views.GenerateQR, name = 'QR'),
	#path('admin/', include("WebForm.urls"))	#assuming this request is coming from a user at /forms, redirect to WebForm ap
]
