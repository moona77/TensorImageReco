# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0004_auto_20151228_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Title', models.CharField(max_length=200)),
                ('Date', models.DateTimeField()),
                ('Url', models.SlugField(unique=True, max_length=100, verbose_name='URL slug')),
                ('Article', models.TextField()),
            ],
            options={
                'ordering': ('Title',),
                'verbose_name': 'News',
            },
        ),
        migrations.RemoveField(
            model_name='network',
            name='project',
        ),
        migrations.RemoveField(
            model_name='nodeset',
            name='project',
        ),
        migrations.AddField(
            model_name='newsdata',
            name='Links',
            field=models.ManyToManyField(to='netgraph.Network'),
        ),
    ]
