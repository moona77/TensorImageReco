#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Nodeset, Network, NewsData, Links
from .form import SearchForm
from django.db.models import Q
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import os, sys, csv, json
import networkx as nx


def home(request):
    """
    Home page of Weblate showing list of projects, stats
    and user links if logged in.
    """




    return render(
        request,
        'index.html'
    )




def poweranalysis(request):
    """
    Home page of Weblate showing list of projects, stats
    and user links if logged in.
    """
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            context = {
                'search_form': search_form,
            }
            context['search_query'] = search_form.cleaned_data['q']
            context['period'] =  search_form.cleaned_data['period']
            context['network'] = Links.objects.filter(node1=search_form.cleaned_data['q']) | Links.objects.filter(node2=search_form.cleaned_data['q'])
            if search_form.cleaned_data['every']:
                context['network'] = Links.objects.filter(node1=search_form.cleaned_data['q']) | Links.objects.filter(node2=search_form.cleaned_data['q'])
            else:
                if search_form.cleaned_data['pol']:
                    context['network'] = Links.objects.filter(Q(node1=context['search_query']), Q(node2attr="Politics")) | Links.objects.filter(Q(node2=context['search_query']), Q(node1attr="Politics"))
                if search_form.cleaned_data['pub']:
                    context['network'] = Links.objects.filter(Q(node1=context['search_query']), Q(node2attr="Public Office")) | Links.objects.filter(Q(node2=context['search_query']), Q(node1attr="Public Office"))
                if search_form.cleaned_data['ent']:
                    context['network'] = Links.objects.filter(Q(node1=context['search_query']), Q(node2attr="Enterprise")) | Links.objects.filter(Q(node2=context['search_query']), Q(node1attr="Enterprise"))
                if search_form.cleaned_data['univ']:
                    context['network'] = Links.objects.filter(Q(node1=context['search_query']), Q(node2attr="Univ/Professor")) | Links.objects.filter(Q(node2=context['search_query']), Q(node1attr="Univ/Professor"))

            if context['period'] == '1w':
                end_date = date.today()
                start_date = end_date - timedelta(days=7)
            elif context['period'] == '1m':
                end_date = date.today()
                start_date = end_date - relativedelta(months=1)
            elif context['period'] == '3m':
                end_date = date.today()
                start_date = end_date - relativedelta(months=3)

            newsall = NewsData.objects.filter(Date__range=(start_date,end_date))
            temc = 0
            for news in newsall:
                if temc==0:
                    temc = news.links_set.all()
                else:
                    temc = temc|news.links_set.all()
            context['network'] = context['network'] & temc

            return render(
                request,
                'poweranalysis.html',
                context
            )

    else:
        search_form = SearchForm()
        context = {
            'search_form': search_form,
        } 
        return render(
            request,
            'poweranalysis.html', 
            context
        )
 

   



def search(request):
    """
    Performs site-wide search on units.
    """
    search_form = SearchForm()
    context = {
        'search_form': search_form,
    }

    if search_form.is_valid():
        context['title'] = search_form.cleaned_data['q']
        context['query_string'] = search_form.urlencode()
        context['search_query'] = search_form.cleaned_data['q']
    else:
        messages.error(request, 'Invalid search query!')

    return render(
        request,
        'poweranalysis.html',
        context
    )
    





def graphedit(request, project):
    obj = get_project(request, project)


    if request.method == 'POST':
        keys = request.POST.keys()


        newnodes = {}
        newlinks = {}
        delnodes = []
        dellinks = []
        for key in keys:

            if key[0:2] == "n_":
                nodeid = key[3:]
                nodetype = key[2]
                if not newnodes.has_key(nodeid):
                    newnodes[nodeid]={}
                if nodetype == "n":
                    newnodes[nodeid]["name"] = request.POST[key]
                elif nodetype == "g":
                    newnodes[nodeid]["group"] = request.POST[key]
                elif nodetype == "i":
                    newnodes[nodeid]["id"] = request.POST[key]

            if key[0:2] == "l_":
                linkid = key[3:]
                linktype = key[2]

                if not newlinks.has_key(linkid):
                    newlinks[linkid]={}

                if linktype == "s":
                    newlinks[linkid]["source"] = request.POST[key]
                elif linktype == "x":
                    newlinks[linkid]["sourceid"] = request.POST[key]
                elif linktype == "t":
                    newlinks[linkid]["target"] = request.POST[key]
                elif linktype == "y":
                    newlinks[linkid]["targetid"] = request.POST[key]
                elif linktype == "w":
                    newlinks[linkid]["weight"] = request.POST[key]

          #  if key[0:2] == "t_":
          #      nodeid = request.POST[key]
          #      delnodes.append(nodeid)


            #if key[0:2] == "d_":
            #    linkid = request.POST[key]
            #    dellinks.append(linkid)





    obj.nodeset_set.all().delete();
    for id, node in newnodes.items():
        obj.nodeset_set.update_or_create(name = node["name"], idnumber = int(node["id"]), group = node["group"] )
       # else:
       #     obj.nodeset_set.update_or_create(name = node[0], idnumber = int(node[1]), group = "2")
       # nodedict[node[1]] = node[0]
       # i+=1

    obj.network_set.all().delete();
    for id, link in newlinks.items():
        obj.network_set.update_or_create(source = link["source"], sourceID = int(link["sourceid"]),
                               target =link["target"], targetID = int(link["targetid"]),
                               weight= float(link["weight"]))


    #for nodeid in delnodes:
     #   obj.nodeset_set.filter(idnumber = int(nodeid)).delete()

    #for linkid in dellinks:

     #   obj.network_set.filter(pk = int(linkid)).delete()



    url = '/projects/'+project+'/'
    return redirect(url)




def analyzer_centrality(request, project):
    projects = Project.objects.all()
    obj = get_project(request, project)


    G = nx.DiGraph()
    nodes = obj.nodeset_set.all()
    links = obj.network_set.all()
    for node in nodes:
        G.add_node(node.idnumber, name = node.name)

    for link in links:
        G.add_edge(link.sourceID, link.targetID, weight = link.weight)

    indeg_centrality = nx.in_degree_centrality(G)
    outdeg_centrality = nx.out_degree_centrality(G)
    deg_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    for key, value in indeg_centrality.items():
        p = obj.nodeset_set.filter(idnumber = key)
        p.update(indegree_centrality = round(value,3))

    for key, value in outdeg_centrality.items():
        p = obj.nodeset_set.filter(idnumber = key)
        p.update(outdegree_centrality = round(value,3))

    for key, value in deg_centrality.items():
        p = obj.nodeset_set.filter(idnumber = key)
        p.update(degree_centrality = round(value,3))

    for key, value in closeness_centrality.items():
        p = obj.nodeset_set.filter(idnumber = key)
        p.update(closeness_centrality = round(value,3))

    for key, value in betweenness_centrality.items():
        p = obj.nodeset_set.filter(idnumber = key)
        p.update(betweenness_centrality = round(value,3))

    nodeset = obj.nodeset_set.all()
    context = {'nodeset' : nodeset,
               'object': obj,
               'projects': projects,
               }
    return render(request, 'centrality.html', context)
