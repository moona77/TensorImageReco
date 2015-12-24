# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=20)),
                ('sourceID', models.IntegerField(default=0)),
                ('target', models.CharField(max_length=20, verbose_name=b'Nodeset')),
                ('targetID', models.IntegerField(default=0)),
                ('weight', models.FloatField()),
            ],
            options={
                'ordering': ['sourceID'],
                'verbose_name': 'Network',
                'verbose_name_plural': 'Networks',
            },
        ),
        migrations.CreateModel(
            name='Nodeset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name to display', max_length=20, verbose_name='node name')),
                ('idnumber', models.IntegerField(default=0)),
                ('group', models.CharField(max_length=20, verbose_name='Group name')),
                ('desc', models.CharField(help_text='Desc to display', max_length=200, verbose_name='descrpition')),
                ('springx', models.FloatField(default=0)),
                ('springy', models.FloatField(default=0)),
                ('indegree_centrality', models.FloatField(default=0)),
                ('outdegree_centrality', models.FloatField(default=0)),
                ('sumdegree_centrality', models.FloatField(default=0)),
                ('incloseness_centrality', models.FloatField(default=0)),
                ('outcloseness_centrality', models.FloatField(default=0)),
                ('sumcloseness_centrality', models.FloatField(default=0)),
                ('betweenness_centrality', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['idnumber'],
                'verbose_name': 'Nodeset',
                'verbose_name_plural': 'Nodesets',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name to display', unique=True, max_length=100, verbose_name='Project name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.AddField(
            model_name='nodeset',
            name='project',
            field=models.ForeignKey(verbose_name='Project', to='netgraph.Project'),
        ),
        migrations.AddField(
            model_name='network',
            name='project',
            field=models.ForeignKey(verbose_name='Project', to='netgraph.Project'),
        ),
    ]
