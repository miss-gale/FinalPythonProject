from __future__ import unicode_literals
from django.db import models
import datetime

class TravelerManager(models.Manager):
    def validate(self, reqData):
        errors = []
        if len(reqData["name"]) < 3:
            errors.append("Name must be at least 3 characters.")
        if len(reqData["username"]) < 3:
                errors.append("Username must be at least 3 characters.")
        if reqData["password"] < 8:
            errors.append("Password must be at least 8 characters.")
        if reqData["password"] != reqData["confirm_pw"]:
            errors.append("Passwords do not match.")
        return errors

class Traveler(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelerManager()

class TripsManager(models.Manager):
    def validate(self, reqData):
        errors = []
        if reqData["destination"] == "":
            errors.append("Destination cannot be empty.")
        if reqData["start_date"] == "":
            errors.append("Start Date cannot be empty.")
        if reqData["end_date"] == "":
            errors.append("End Date cannot be empty.")
        if reqData["description"] == "":
            errors.append("Description cannot be empty.")
        start = datetime.datetime.strptime(reqData["start_date"], "%Y-%m-%d")
        end = datetime.datetime.strptime(reqData["end_date"], "%Y-%m-%d")
        today = datetime.datetime.today()
        if start < today:
            errors.append("Start Date cannot be in the past.")
        if end < start:
            errors.append("End Date cannot be before the Start Date.")
        return errors

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    created_by = models.ForeignKey(Traveler, related_name="host")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripsManager()

class Plans(models.Model):
    traveler = models.ForeignKey(Traveler, related_name="rsvpd")
    trip = models.ForeignKey(Trips, related_name="travelers_joined")
