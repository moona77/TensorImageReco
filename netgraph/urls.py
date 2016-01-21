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
        r'^poweranalysis/$',
        views.poweranalysis,
        name='poweranalysis',
    ),


    url(
        r'^analyzer/' + PROJECT + 'centrality$',
        views.analyzer_centrality,
        name='analyzer_centrality',
    ),




    url(
        r'^projects/' + PROJECT + 'graphedit/$',
        views.graphedit,
        name='graphedit',
    ),

]