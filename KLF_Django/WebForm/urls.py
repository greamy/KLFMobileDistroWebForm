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
	path('get-location-data/', views.get_locations, name='getLocations'),
	path('post-location-data/', views.create_site, name='postLocations'),
	path('delete-location-data/', views.delete_site, name='deleteSite'),
	path('get-submission-table/', views.get_submission_table, name='getSubmissionTable'),
	path('get-form-settings/', views.get_form_fields, name='getFormSettings'),
	path('remove-form-field/', views.remove_form_field, name="removeFormField"),
	path('post-form-settings/', views.save_form_fields, name='postFormSettings'),
	path('get-excel-file/', views.get_excel_file, name='getExcel'),
	path('change-username/', views.change_username, name='changeUsername'),
	path('change-password/', views.change_password, name='changePassword'),
	path('admin/login/', views.admin_login, name='admin_login'),
	path('admin/logout/', views.logout_user, name='admin_logout'),
	path('admin/', views.admin, name='admin'),
	path('<str:site_name>/submit/', views.submit, name='submit'),
	path('QR/', views.generate_QR, name='QR'),
	path('<str:site>/', views.index, name="index")  # path(route, view)
	# path('admin/', include("WebForm.urls"))	#assuming this request is coming from a user at /forms, redirect to WebForm ap
]
