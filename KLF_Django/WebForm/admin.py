from django.contrib import admin
from .models import Location, Site, Submission

# Register your models here.
admin.site.register(Location)
admin.site.register(Site)
admin.site.register(Submission)