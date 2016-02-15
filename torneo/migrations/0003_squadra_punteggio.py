# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0002_auto_20160215_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadra',
            name='punteggio',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
