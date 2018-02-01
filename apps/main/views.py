from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from . models import *
import bcrypt, datetime


def index(request):
    return render(request, "main/index.html")


def register(request):
    errors = Traveler.objects.validate(request.POST)
    if len(errors):
        for error in errors:
            messages.warning(request, error)
        return redirect("/")
    else:
        hash_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        Traveler.objects.create(name=request.POST["name"], username=request.POST["username"], password=hash_pw)
        request.session["current_user"] = request.POST["name"]
        request.session["current_user_id"] = Traveler.objects.get(name=request.POST["name"]).id
    return redirect("/travels")


def login(request):
    current_user = Traveler.objects.get(username=request.POST["username"])
    if(bcrypt.checkpw(request.POST["password"].encode(), current_user.password.encode())):
        request.session["current_user"] = current_user.name
        request.session["current_user_id"] = current_user.id
        return redirect("/travels")
    else:
        return redirect("/")


def logout(request):
    for s_key in request.session.keys():
        del request.session[s_key]
    return redirect("/")


def travels(request):
    context = {
        "current_traveler": Traveler.objects.get(id=request.session["current_user_id"]),
        "users_trips": Trips.objects.filter(created_by=Traveler.objects.get(id=request.session["current_user_id"])),
        "all_plans": Trips.objects.all().exclude(created_by=Traveler.objects.get(id=request.session["current_user_id"]))
    }
    return render(request, "main/travels.html", context)


def add(request):
    return render(request, "main/add.html")


def new_trip(request):
    errors = Trips.objects.validate(request.POST)
    if len(errors):
        for error in errors:
            error_num = 1
            messages.add_message(request, error_num, error)
            error_num += error_num
            print error
        return redirect("/travels/add")
    else:
        Trips.objects.create(destination=request.POST["destination"], start_date=request.POST["start_date"], end_date=request.POST["end_date"], description=request.POST["description"], created_by=Traveler.objects.get(id=request.session["current_user_id"]))
    return redirect("/travels")


def destination(request, trip_id):
    context = {
        "this_destination": Trips.objects.get(id=trip_id)
    }
    return render(request, "main/destination.html", context)


def join(request, trip_id):
    current_traveler = Traveler.objects.get(id=request.session["current_user_id"])
    Plans.objects.create(traveler=current_traveler, trip=Trips.objects.get(id=trip_id))
    return redirect("/travels")
