from django.conf.urls import url

from . import views

PROJECT = r'(?P<project>[^/]+)/'

urlpatterns = [
    url(
        r'^$',
        views.home,
        name='home',
    ),

    url(
        r'^imageanalysis/$',
        views.poweranalysis,
        name='poweranalysis',
    ),


]