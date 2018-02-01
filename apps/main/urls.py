from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travels$', views.travels),
    url(r'^main/register$', views.register),
    url(r'^main/login$', views.login),
    url(r'^main/logout$', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^travels/add/new_trip$', views.new_trip),
    url(r'^travels/destination/(?P<trip_id>\d+)$', views.destination),
    url(r'^travels/destination/join/(?P<trip_id>\d+)$', views.join),
]
