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
        r'^projects/$',
        views.home,
        name='home'
    ),
    url(
        r'^projects/' + PROJECT + '$',
        views.show_project,
        name='project',
    ),

    url(
        r'^newproject/$',
        views.show_newproject,
        name='show_newproject',
    ),

    url(
        r'^uploadcsvfile/$',
        views.newproject,
        name='newproject',
    ),

    url(
        r'^newblank/$',
        views.newblank,
        name='newblank',
    ),

    url(
        r'^analyzer/' + PROJECT + 'centrality$',
        views.analyzer_centrality,
        name='analyzer_centrality',
    ),

    url(
        r'^projects/' + PROJECT + 'deletenode/$',
        views.delete_node,
        name='delete_node',
    ),

    url(
        r'^projects/' + PROJECT + 'deletelink/$',
        views.delete_link,
        name='delete_link',
    ),

    url(
        r'^projects/' + PROJECT + 'graphedit/$',
        views.graphedit,
        name='graphedit',
    ),

]