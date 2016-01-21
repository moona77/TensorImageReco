# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0006_auto_20160120_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node1', models.CharField(max_length=20)),
                ('node2', models.CharField(max_length=20, verbose_name=b'Nodeset')),
            ],
            options={
                'ordering': ['node1'],
                'verbose_name': 'Link',
            },
        ),
        migrations.RemoveField(
            model_name='newsdata',
            name='Links',
        ),
        migrations.AddField(
            model_name='links',
            name='NewsData',
            field=models.ForeignKey(to='netgraph.NewsData'),
        ),
    ]
