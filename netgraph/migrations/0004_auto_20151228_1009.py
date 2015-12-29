# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0003_auto_20151224_1033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nodeset',
            old_name='incloseness_centrality',
            new_name='closeness_centrality',
        ),
        migrations.RenameField(
            model_name='nodeset',
            old_name='outcloseness_centrality',
            new_name='degree_centrality',
        ),
        migrations.RemoveField(
            model_name='nodeset',
            name='sumcloseness_centrality',
        ),
        migrations.RemoveField(
            model_name='nodeset',
            name='sumdegree_centrality',
        ),
    ]
