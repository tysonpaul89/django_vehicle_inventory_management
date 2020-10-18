
"""Module contiains models for Vehicle"""
from django.db import models
from django.contrib.auth import get_user_model

FUEL_TYPE_CHOICES = (
    ('P','Petrol'),
    ('D','Diesel'),
)

class VehicleType(models.Model):
    """Model to store the vehicle type like seadan, hatchback, etc."""
    type = models.CharField(max_length=45)

    def __str__(self):
        return self.type


class Vehicle(models.Model):
    """Model to store the vehicle details"""
    vehicle_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    fuel_type = models.CharField(max_length=1, default='P', choices=FUEL_TYPE_CHOICES)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
