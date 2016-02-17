# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0006_squadra_confermata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partita',
            name='done',
        ),
        migrations.RemoveField(
            model_name='partita',
            name='punteggio1',
        ),
        migrations.RemoveField(
            model_name='partita',
            name='punteggio2',
        ),
        migrations.AddField(
            model_name='partita',
            name='punteggio11',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partita',
            name='punteggio12',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partita',
            name='punteggio21',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partita',
            name='punteggio22',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partita',
            name='stato',
            field=models.CharField(default=b'INC', max_length=3, choices=[(b'INC', b'Partita non disputata'), (b'AT1', b'In attesa di conferma dalla prima squadra'), (b'AT2', b'In attesa di conferma della seconda squadra'), (b'DON', b'Punteggio confermato')]),
            preserve_default=True,
        ),
    ]
