#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Nodeset(models.Model):
    name = models.CharField(
        verbose_name=ugettext_lazy('node name'),
        max_length=20,
        help_text=ugettext_lazy('Name to display')
    )

    category = models.CharField(
        max_length = 20,
        verbose_name=ugettext_lazy('Group name'),
    )

    isquery = models.BooleanField(
        default=False
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

    sourceid = models.IntegerField(
        default=0
        #max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )

    target = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )


    targetid = models.IntegerField(
        default=0
        #max_length=100,
        #verbose_name=ugettext_lazy('target name')
    )

    weight = models.IntegerField(
        default= 1
    )

    #News = models.ManyToManyField(NewsData)

    class Meta(object):
        ordering = ['pk']
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

    Media = models.CharField(
        max_length=200,
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


class Keyword(models.Model):
    node = models.CharField(
        max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )

    nodeattr = models.ForeignKey(
        Nodeset
    )

    NewsData = models.ForeignKey(NewsData)


    class Meta(object):
        ordering = ['nodeattr__pk']
        verbose_name = ugettext_lazy('keyword')


    def __unicode__(self):
        return _(self.node)


class Links(models.Model):
    node1 = models.IntegerField(
        #max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )

    node2 = models.IntegerField(
        #max_length=100,
        #verbose_name=ugettext_lazy('source name'),
    )

    link = models.ForeignKey(
        Network
    )

    news = models.ForeignKey(
        NewsData
    )


    class Meta(object):

        verbose_name = ugettext_lazy('links')


    def __unicode__(self):
        return _(self.node1 + "--"+self.node2)


