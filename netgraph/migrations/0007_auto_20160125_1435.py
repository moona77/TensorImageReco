# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0006_nodeset_isquery'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nodeset',
            old_name='group',
            new_name='category',
        ),
    ]
