from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Paasenger

# Create your views here.


def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")

    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Paasenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)


def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Paasenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flight/error.html", {"message": "No Selection"})
    except Flight.DoesNotExist:
        return render(request, "flight/error.html", {"message": "No Flight"})
    except Paasenger.DoesNotExist:
        return render(request, "flight/error.html", {"message": "No Passenger."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
