# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0005_squadra_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadra',
            name='confermata',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
