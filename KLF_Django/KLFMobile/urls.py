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
from django.urls import include, path

urlpatterns = [

    path('djangoadmin/', admin.site.urls),

    path('form/', include("WebForm.urls"))	#assuming this request is coming from a user at /forms, redirect to WebForm app
    						#testing means running the server then going to /form, this will populate the form
    						#with the message contained in WebForm.views.py
]
