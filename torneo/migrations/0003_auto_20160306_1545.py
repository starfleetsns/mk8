# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0002_datiutente'),
    ]

    operations = [
        migrations.AddField(
            model_name='partita',
            name='campionato',
            field=models.BooleanField(default=True, verbose_name=b'Partita di campionato'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partita',
            name='gare',
            field=models.IntegerField(default=8, verbose_name=b'Numero di gare disputate'),
            preserve_default=False,
        ),
    ]
