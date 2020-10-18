from django.contrib import admin
from .models import VehicleType, Vehicle

class VehicleTypeAdmin(admin.ModelAdmin):
    pass

class VehicleAdmin(admin.ModelAdmin):
    pass

admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(Vehicle, VehicleAdmin)
