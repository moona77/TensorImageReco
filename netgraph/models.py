#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Nodeset(models.Model):
    name = models.CharField(
        verbose_name=ugettext_lazy('node name'),
        max_length=20,
        help_text=ugettext_lazy('Name to display')
    )

    group = models.CharField(
        max_length = 20,
        verbose_name=ugettext_lazy('Group name'),
    )

    x =models.FloatField(
        default=0
    )
    y =models.FloatField(
        default=0
    )

    indegree_centrality = models.FloatField(
        default = 0
    )

    outdegree_centrality = models.FloatField(
        default = 0
    )

    closeness_centrality = models.FloatField(
        default = 0
    )

    betweenness_centrality = models.FloatField(
        default = 0
    )


    class Meta(object):
        ordering = ['pk']
        verbose_name = ugettext_lazy('Nodeset')
        verbose_name_plural = ugettext_lazy('Nodesets')

    def __unicode__(self):
        return _(self.name)




class Network(models.Model):
    source = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )

    sourceID = models.IntegerField(
        default=0,
        null=False
    )

    target = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('target name')
    )

    targetID = models.IntegerField(
        default=0,
        null=False
    )

    weight = models.CharField(
        max_length=20,
    )


    #News = models.ManyToManyField(NewsData)

    class Meta(object):
        ordering = ['sourceID']
        verbose_name = ugettext_lazy('Network')
        verbose_name_plural = ugettext_lazy('Networks')

    def __unicode__(self):
        return _(self.source+"->"+self.target)


class NewsData(models.Model):
    Title = models.CharField(
        max_length=200,
        #verbose_name=ugettext_lazy('source name'),
    )

    Date = models.DateTimeField(

    )

    Url = models.URLField(
        verbose_name=ugettext_lazy('URL'),
        db_index=True, unique=True,
        max_length=200,
        #verbose_name=ugettext_lazy('target name')
    )

    Article = models.TextField(
    )


    class Meta(object):
        ordering = ('Title',)
        verbose_name = ugettext_lazy('New')

    def __unicode__(self):
        return _(self.Title)


class Links(models.Model):
    node1 = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )

    node1attr = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )


    node2 = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('target name')
    )

    node2attr = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )

    NewsData = models.ForeignKey(NewsData)


    #News = models.ManyToManyField(NewsData)

    class Meta(object):
        ordering = ['node1']
        verbose_name = ugettext_lazy('Link')


    def __unicode__(self):
        return _(self.node1+"-"+self.node2)





