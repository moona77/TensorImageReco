from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Nodeset, Network
 
import os, sys, csv, json
import networkx as nx



def home(request):
    """
    Home page of Weblate showing list of projects, stats
    and user links if logged in.
    """

    projects = Project.objects.all()


    return render(
        request,
        'index.html',
        {
            'projects': projects,
        }
    )



def get_project(request, project):
    '''
    Returns project matching parameters.
    '''
    project = get_object_or_404(
        Project,
        slug = project,
    )

    return project


def show_project(request, project):

    project = get_project(request, project)
    projects = Project.objects.all()
    #print Nodeset.objects.all()


    return render(
        request,
        'project.html',
        {
            'project': project,
            'projects': projects,

        }
    )

def show_newproject(request):
    projects = Project.objects.all()
    return render(request, "newproject.html", {'projects': projects,})





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



def delete_node(request, project):
    obj = get_project(request, project)

    if request.method == 'POST':
        keys = request.POST.keys()
        try:
            keys.remove(u'csrfmiddlewaretoken')
            keys.remove(u'checkallnode')
        except:
            pass
        print keys

        for key in keys:
            print key
            u = request.POST[key]
            obj.nodeset_set.filter(idnumber = int(u)).delete()
            obj.network_set.filter(sourceID = int(u)).delete()
            obj.network_set.filter(targetID = int(u)).delete()




    url = '/projects/'+project+'/'
    return redirect(url)

def delete_link(request, project):
    obj = get_project(request, project)

    if request.method == 'POST':
        keys = request.POST.keys()
        try:
            keys.remove(u'csrfmiddlewaretoken')
            keys.remove(u'checkalllink')
        except:
            pass
        print keys

        for key in keys:
            print key
            u = request.POST[key]
            obj.network_set.filter(pk = int(u)).delete()





    url = '/projects/'+project+'/'
    return redirect(url)


def newproject(request):



  if request.method == 'POST':


    f = request.FILES['upload_file']


    project = request.POST['projectname']

    path = '/home/moon/.virtualenvs/myproject/data/'

    dataset = [row for row in csv.reader(f.read().splitlines())] # csv file parsing
    handle_uploaded_file(f, path)  #file save



    Project.objects.update_or_create(name = project, slug =project)
    obj = get_project(request, project)



    nodes =[]
    for data in dataset:
        nodes.append(data[0])
        nodes.append(data[1])
    nodeset = list(set(nodes))



    nodedict = {}

    for i, node in enumerate(nodeset):
        obj.nodeset_set.update_or_create(name = node, idnumber = i, group = "0")
        nodedict[node] = i



    #obj.network_set.all().delete()
    for link in dataset:
        obj.network_set.update_or_create(source = link[0], sourceID = nodedict[link[0]],
                               target = link[1], targetID = nodedict[link[1]],
                               weight= float(link[2]))



    G = nx.Graph()
    nodes = obj.nodeset_set.all()
    links = obj.network_set.all()


    for node in nodes:
        G.add_node(node.idnumber, name = node.name)

    for link in links:
        G.add_edge(link.sourceID, link.targetID, weight = link.weight)


    pos = nx.spring_layout(G)

    for key, value in pos.items():
        obj.nodeset_set.filter(idnumber = key).update(springx = value[0], springy=value[1])



    """
    for i, path in enumerate(filepath_nodeset):
        try:
            nodes = dataset.create_nodeset(nodesetname[i])
        except:
            nodes = dataset.get_nodeset(nodesetname[i])
        data = pd.read_csv(path)
        attlist = data.columns.values
        nodesetImport = NodesetImportFormat(',')

        nodesetImport.set_id(1)
        column_num=1
        print attlist
        for att in attlist:
            if data[att].dtypes =='object':
                nodesetImport.set_string(column_num, str(att))
                print column_num, ", string, ", att
            if data[att].dtypes== 'int64':
                nodesetImport.set_int(column_num, str(att))
                print column_num, ", int, ", att
            if data[att].dtypes== 'float64':
                nodesetImport.set_double(column_num, str(att))
                print column_num, ", double, ", att
            column_num += 1

        #print nodesetImport
        nodesetImport.set_skip_rows(1)
        nodes.run_import(path, nodesetImport)

    """


  url = '/projects/'+project+'/'
  return redirect(url)


def newblank(request):

    project = request.POST['projectname']
    print project

    if request.method == 'POST':

        project = request.POST['projectname']

        Project.objects.update_or_create(name = project, slug =project)



        url = '/projects/'+project+'/'
    return redirect(url)












def handle_uploaded_file(f, path):
  if not os.path.exists(path):
    os.mkdir(path)
  fn = path + 'temp.csv'
  with open(fn, 'wb+') as destination:
    for chunk in f.chunks():
        destination.write(chunk)


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

    for key, value in indeg_centrality.items():
        p = obj.nodeset_set.filter(idnumber = key)
        p.update(indegree_centrality = value)

    for key, value in outdeg_centrality.items():
        p = obj.nodeset_set.filter(idnumber = key)
        p.update(outdegree_centrality = value)


    nodeset = obj.nodeset_set.all()
    context = {'nodeset' : nodeset,
               'object': obj,
                'project': obj,
               }
    return render(request, 'centrality.html', context)
