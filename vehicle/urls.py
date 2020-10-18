from os import name
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.vehicle_listing, name="home"),
    path('vehicle-listing', views.vehicle_listing_data, name="vehicle-listing"),
    path('create', views.create_vechicle, name="vehicle-create"),
    path('edit/<int:vehicle_id>', views.edit_vechicle, name="vehicle-edit"),
    path('delete/<int:vehicle_id>', views.delete_vechicle, name="vehicle-delete"),
]