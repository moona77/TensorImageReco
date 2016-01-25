# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node1', models.CharField(max_length=100)),
                ('node2', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'links',
            },
        ),
        migrations.AlterModelOptions(
            name='keyword',
            options={'ordering': ['nodeattr__pk'], 'verbose_name': 'keyword'},
        ),
        migrations.AlterModelOptions(
            name='network',
            options={'ordering': ['source'], 'verbose_name': 'Network', 'verbose_name_plural': 'Networks'},
        ),
        migrations.RemoveField(
            model_name='network',
            name='sourceID',
        ),
        migrations.RemoveField(
            model_name='network',
            name='targetID',
        ),
        migrations.AlterField(
            model_name='network',
            name='weight',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='links',
            name='link',
            field=models.ForeignKey(to='netgraph.Network'),
        ),
        migrations.AddField(
            model_name='links',
            name='news',
            field=models.ForeignKey(to='netgraph.NewsData'),
        ),
    ]
