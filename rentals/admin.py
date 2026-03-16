from django.contrib import admin
from .models import Bike, Renter, Rental

admin.site.register(Bike)
admin.site.register(Renter)
admin.site.register(Rental)
