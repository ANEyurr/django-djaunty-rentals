from django.shortcuts import render

from .models import Bike


def bike_list(request):
    bikes = Bike.objects.all()
    return render(request, "rentals/bike_list.html", {"bikes": bikes})
