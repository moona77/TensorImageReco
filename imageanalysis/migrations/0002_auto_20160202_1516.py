# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageanalysis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='NewsData',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='nodeattr',
        ),
        migrations.DeleteModel(
            name='Network',
        ),
        migrations.DeleteModel(
            name='Keyword',
        ),
        migrations.DeleteModel(
            name='NewsData',
        ),
        migrations.DeleteModel(
            name='Nodeset',
        ),
    ]
