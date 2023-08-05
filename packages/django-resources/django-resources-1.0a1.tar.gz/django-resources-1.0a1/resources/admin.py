from django.contrib import admin

from resources.models import Resource
admin.site.register(Resource)

from resources.models import MergedResource
admin.site.register(MergedResource)
