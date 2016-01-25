# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0004_auto_20160122_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='network',
            options={'ordering': ['pk'], 'verbose_name': 'Network', 'verbose_name_plural': 'Networks'},
        ),
    ]
