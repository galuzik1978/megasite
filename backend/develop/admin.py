from django.contrib import admin

# Register your models here.
from develop.models import Division, Region, Machine

admin.site.register(Division)
admin.site.register(Region)
admin.site.register(Machine)
