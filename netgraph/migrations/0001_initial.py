# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['node'],
                'verbose_name': 'keyword',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=100)),
                ('sourceID', models.IntegerField(default=0)),
                ('target', models.CharField(max_length=100)),
                ('targetID', models.IntegerField(default=0)),
                ('weight', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['sourceID'],
                'verbose_name': 'Network',
                'verbose_name_plural': 'Networks',
            },
        ),
        migrations.CreateModel(
            name='NewsData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Title', models.CharField(max_length=200)),
                ('Date', models.DateTimeField()),
                ('Url', models.URLField(unique=True, verbose_name='URL', db_index=True)),
                ('Article', models.TextField()),
            ],
            options={
                'ordering': ('Title',),
                'verbose_name': 'New',
            },
        ),
        migrations.CreateModel(
            name='Nodeset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name to display', max_length=20, verbose_name='node name')),
                ('group', models.CharField(max_length=20, verbose_name='Group name')),
                ('x', models.FloatField(default=0)),
                ('y', models.FloatField(default=0)),
                ('indegree_centrality', models.FloatField(default=0)),
                ('outdegree_centrality', models.FloatField(default=0)),
                ('closeness_centrality', models.FloatField(default=0)),
                ('betweenness_centrality', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['pk'],
                'verbose_name': 'Nodeset',
                'verbose_name_plural': 'Nodesets',
            },
        ),
        migrations.AddField(
            model_name='keyword',
            name='NewsData',
            field=models.ForeignKey(to='netgraph.NewsData'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='nodeattr',
            field=models.ForeignKey(to='netgraph.Nodeset'),
        ),
    ]
