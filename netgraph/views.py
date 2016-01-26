# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Nodeset, Network, NewsData, Keyword, Links
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

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            context = {'search_form': search_form, 'search_query': search_form.cleaned_data['q'],
                       'period': search_form.cleaned_data['period'],
                       'network': Keyword.objects.filter(node=search_form.cleaned_data['q'])}

            end_date = date.today()+relativedelta(days=1)
            if context['period'] == '1w':
                start_date = end_date - relativedelta(days=7)
            elif context['period'] == '1m':
                start_date = end_date - relativedelta(months=1)
            elif context['period'] == '3m':
                start_date = end_date - relativedelta(months=3)

            newsall = NewsData.objects.filter(Date__range=(start_date, end_date))

            Network.objects.all().delete()
            Links.objects.all().delete()
            temp = set()
            graphtemp ={}

            for news in newsall:
                key = news.keyword_set.filter(node=context["search_query"])
                if key.count()>0:
                    #조건제한이 없을때
                    if search_form.cleaned_data['every']:

                        key_all = news.keyword_set.all()
                        for key1 in key_all:

                            for key2 in key_all:
                                if(key1.nodeattr.pk<key2.nodeattr.pk):
                                    obj, created = Network.objects.get_or_create(source = key1.node, sourceid = key1.nodeattr.pk, target = key2.node, targetid = key2.nodeattr.pk, defaults = {'weight':1})
                                    if not created:
                                        Network.objects.filter(pk=obj.pk).update(weight =obj.weight+1)
                                    Links.objects.create(node1 = key1.nodeattr.pk, node2 = key2.nodeattr.pk, link= obj, news= news)

                    #조건 제한이 있을 경우
                    else:
                        if search_form.cleaned_data['pol']:
                            group = "정치인"
                        if search_form.cleaned_data['pub']:
                            group = "공공기관"
                        if search_form.cleaned_data['ent']:
                            group = "기업"
                        if search_form.cleaned_data['univ']:
                            group = "대학/교수"

                        key_all = news.keyword_set.filter(node=context["search_query"])|news.keyword_set.filter(nodeattr__category=group)
                        for key1 in key_all:
                            #temp.add(key1.nodeattr)
                            for key2 in key_all:
                                if(key1.nodeattr.pk<key2.nodeattr.pk):
                                    obj, created = Network.objects.get_or_create(source = key1.node, sourceid = key1.nodeattr.pk, target = key2.node, targetid = key2.nodeattr.pk, weight =1)
                                    if not created:
                                        Network.objects.filter(pk=obj.pk).update(weight =obj.weight+1)
                                    Links.objects.create(node1 = key1.nodeattr.pk, node2 = key2.nodeattr.pk, link= obj, news= news)

            temp = list(temp)
            c = set()

            a = Network.objects.all()

            for link in a:
                if link.weight < 2:
                    link.delete()
                else:
                    c.add(Nodeset.objects.get(pk=link.sourceid))
                    c.add(Nodeset.objects.get(pk=link.targetid))
            c = list(c)
            #print c

            context['network'] = Network.objects.all()
            #print context['network']


            G = nx.Graph()
            nodes = c
            links = context['network']
            for node in nodes:
                G.add_node(node.pk, name = node.name)

            for link in links:
                G.add_edge(link.sourceid, link.targetid, weight = link.weight)

            indeg_centrality = nx.betweenness_centrality(G)
            pos = nx.shell_layout(G)


            max_x=0
            min_x=100000
            max_y=0
            min_y=100000

            for node in c:
                if pos[node.pk][0]>max_x:
                    max_x = pos[node.pk][0]
                if pos[node.pk][0]<min_x:
                    min_x = pos[node.pk][0]
                if pos[node.pk][1]>max_y:
                    max_y = pos[node.pk][1]
                if pos[node.pk][1]<min_y:
                    min_y = pos[node.pk][1]

            for node in c:
                if node.name == context["search_query"]:
                    node.isquery = True
               # print node.name,pos[node.pk][0],pos[node.pk][1]
                node.x =(pos[node.pk][0]-min_x)/(max_x-min_x)
                node.y =(pos[node.pk][1]-min_y)/(max_y-min_y)

            context['nodeset'] = c
            #print temp
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


def weight(request, pk):
    """
    Performs site-wide search on units.
    """
    search_form = SearchForm()
    context = {
        'search_form': search_form,
    }

    context['links'] = Network.objects.get(pk=pk).links_set.all()


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
                    newnodes[nodeid] = {}
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
                    newlinks[linkid] = {}

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


                    # if key[0:2] == "d_":
                    #    linkid = request.POST[key]
                    #    dellinks.append(linkid)

    obj.nodeset_set.all().delete();
    for id, node in newnodes.items():
        obj.nodeset_set.update_or_create(name=node["name"], idnumber=int(node["id"]), group=node["group"])
        # else:
        #     obj.nodeset_set.update_or_create(name = node[0], idnumber = int(node[1]), group = "2")
        # nodedict[node[1]] = node[0]
        # i+=1

    obj.network_set.all().delete();
    for id, link in newlinks.items():
        obj.network_set.update_or_create(source=link["source"], sourceID=int(link["sourceid"]),
                                         target=link["target"], targetID=int(link["targetid"]),
                                         weight=float(link["weight"]))


        # for nodeid in delnodes:
        #   obj.nodeset_set.filter(idnumber = int(nodeid)).delete()

        # for linkid in dellinks:

        #   obj.network_set.filter(pk = int(linkid)).delete()

    url = '/projects/' + project + '/'
    return redirect(url)


def analyzer_centrality(request, project):
    projects = Project.objects.all()
    obj = get_project(request, project)

    G = nx.DiGraph()
    nodes = obj.nodeset_set.all()
    links = obj.network_set.all()
    for node in nodes:
        G.add_node(node.idnumber, name=node.name)

    for link in links:
        G.add_edge(link.sourceID, link.targetID, weight=link.weight)

    indeg_centrality = nx.in_degree_centrality(G)
    outdeg_centrality = nx.out_degree_centrality(G)
    deg_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    for key, value in indeg_centrality.items():
        p = obj.nodeset_set.filter(idnumber=key)
        p.update(indegree_centrality=round(value, 3))

    for key, value in outdeg_centrality.items():
        p = obj.nodeset_set.filter(idnumber=key)
        p.update(outdegree_centrality=round(value, 3))

    for key, value in deg_centrality.items():
        p = obj.nodeset_set.filter(idnumber=key)
        p.update(degree_centrality=round(value, 3))

    for key, value in closeness_centrality.items():
        p = obj.nodeset_set.filter(idnumber=key)
        p.update(closeness_centrality=round(value, 3))

    for key, value in betweenness_centrality.items():
        p = obj.nodeset_set.filter(idnumber=key)
        p.update(betweenness_centrality=round(value, 3))

    nodeset = obj.nodeset_set.all()
    context = {'nodeset': nodeset,
               'object': obj,
               'projects': projects,
               }
    return render(request, 'centrality.html', context)
