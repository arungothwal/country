from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [

    url(r'^country/data', Country_data.as_view()),
    url(r'^country/update/(?P<pk>\d+)/$', Country_data.as_view()),
    url(r'^country/delete/(?P<pk>\d+)/$', Country_data.as_view()),

    url(r'^state/data', State_data.as_view()),
    url(r'^state/update/(?P<pk>\d+)/$', State_data.as_view()),
    url(r'^state/delete/(?P<pk>\d+)/$', State_data.as_view()),

    url(r'^city/data', City_data.as_view()),
    url(r'^city/update/(?P<pk>\d+)/$', City_data.as_view()),
    url(r'^city/delete/(?P<pk>\d+)/$', City_data.as_view()),

    url(r'^town/data', Town_data.as_view()),
    url(r'^town/update/(?P<pk>\d+)/$', Town_data.as_view()),
    url(r'^town/delete/(?P<pk>\d+)/$', Town_data.as_view()),

    url(r'^person/data', Persons.as_view()),
    url(r'^person/update/(?P<pk>\d+)/$', Persons.as_view()),
    url(r'^person/delete/(?P<pk>\d+)/$', Persons.as_view()),

    url(r'^data', Person_data.as_view()),
    url(r'^update/(?P<pk>\d+)/$', Person_data.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', Person_data.as_view()),

    url(r'^person_data', PersonListView.as_view()),

]