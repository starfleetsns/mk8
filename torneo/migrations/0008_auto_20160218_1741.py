# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0007_auto_20160217_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadra',
            name='lunghezza',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partita',
            name='punteggio11',
            field=models.IntegerField(default=0, verbose_name=b'Prima squadra, primo giocatore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partita',
            name='punteggio12',
            field=models.IntegerField(default=0, verbose_name=b'Prima squadra, secondo giocatore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partita',
            name='punteggio21',
            field=models.IntegerField(default=0, verbose_name=b'Seconda squadra, primo giocatore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partita',
            name='punteggio22',
            field=models.IntegerField(default=0, verbose_name=b'Seconda squadra, secondo giocatore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partita',
            name='squadra1',
            field=models.ForeignKey(related_name='partite1', verbose_name=b'Prima squadra', to='torneo.Squadra'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partita',
            name='squadra2',
            field=models.ForeignKey(related_name='partite2', verbose_name=b'Seconda squadra', to='torneo.Squadra'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='squadra',
            name='giocatore1',
            field=models.CharField(max_length=200, verbose_name=b'Primo giocatore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='squadra',
            name='giocatore2',
            field=models.CharField(max_length=200, verbose_name=b'Secondo giocatore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='squadra',
            name='nome',
            field=models.CharField(max_length=200, verbose_name=b'Nome della squadra'),
            preserve_default=True,
        ),
    ]
