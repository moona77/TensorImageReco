from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Project(models.Model):
    name = models.CharField(
        verbose_name=ugettext_lazy('Project name'),
        max_length=100,
        unique=True,
        help_text=ugettext_lazy('Name to display')
    )

    slug = models.SlugField(
        verbose_name=ugettext_lazy('URL slug'),
        db_index=True, unique=True,
        max_length=100,
        help_text=ugettext_lazy('Name used in URLs and file names.')
    )

    class Meta(object):
        ordering = ['name']
        verbose_name = ugettext_lazy('Project')
        verbose_name_plural = ugettext_lazy('Projects')

    def __unicode__(self):
        return _(self.name)



class Nodeset(models.Model):
    name = models.CharField(
        verbose_name=ugettext_lazy('node name'),
        max_length=20,
        help_text=ugettext_lazy('Name to display')
    )

    idnumber = models.IntegerField(
        default= 0,
        null = False
    )

    group = models.CharField(
        max_length = 20,
        verbose_name=ugettext_lazy('Group name'),
    )

    desc = models.CharField(
        verbose_name=ugettext_lazy('descrpition'),
        max_length=200,
        help_text=ugettext_lazy('Desc to display')
    )

    springx =models.FloatField(
        default=0
    )
    springy =models.FloatField(
        default=0
    )

    indegree_centrality = models.FloatField(
        default = 0
    )

    outdegree_centrality = models.FloatField(
        default = 0
    )

    sumdegree_centrality = models.FloatField(
        default = 0
    )

    incloseness_centrality = models.FloatField(
        default = 0
    )

    outcloseness_centrality = models.FloatField(
        default = 0
    )

    sumcloseness_centrality = models.FloatField(
        default = 0
    )

    betweenness_centrality = models.FloatField(
        default = 0
    )


    project = models.ForeignKey(
        Project,
        verbose_name=ugettext_lazy('Project'),
    )

    class Meta(object):
        ordering = ['idnumber']
        verbose_name = ugettext_lazy('Nodeset')
        verbose_name_plural = ugettext_lazy('Nodesets')

    def __unicode__(self):
        return _(self.name)




class Network(models.Model):
    source = models.CharField(
        max_length=20,
        #verbose_name=ugettext_lazy('source name'),
    )

    sourceID = models.IntegerField(
        default=0,
        null=False
    )

    target = models.CharField(
    	'Nodeset',
        max_length=20,
        #verbose_name=ugettext_lazy('target name')
    )

    targetID = models.IntegerField(
        default=0,
        null=False
    )

    weight = models.CharField(
        max_length=20,
    )


    project = models.ForeignKey(
        'Project',
        verbose_name=ugettext_lazy('Project'),
    )

    class Meta(object):
        ordering = ['sourceID']
        verbose_name = ugettext_lazy('Network')
        verbose_name_plural = ugettext_lazy('Networks')

    def __unicode__(self):
        return _(self.source+"->"+self.target)

