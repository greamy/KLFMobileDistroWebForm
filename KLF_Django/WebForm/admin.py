from django.contrib import admin
from .models import Location, Site, Submission, Field, Description

class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


# Register your models here.
admin.site.register(Location)
admin.site.register(Site)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Field)
admin.site.register(Description)
