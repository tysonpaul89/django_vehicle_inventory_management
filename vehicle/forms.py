"""Module contains models for the vehicle app"""
from django.forms import ModelForm, HiddenInput
from .models import Vehicle

class VehicleForm(ModelForm):
    """Form model for Vehicle model"""

    class Meta:
        model = Vehicle
        fields = ("name", "model", "price", "fuel_type", "vehicle_type", "user")
        widgets = {'user': HiddenInput()}