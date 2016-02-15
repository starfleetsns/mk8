# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('punteggio1', models.IntegerField(default=0)),
                ('punteggio2', models.IntegerField(default=0)),
                ('done', models.BooleanField(default=False)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Squadra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('giocatore1', models.CharField(max_length=200)),
                ('giocatore2', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='partita',
            name='squadra1',
            field=models.ForeignKey(to='torneo.Squadra', related_name='partite1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partita',
            name='squadra2',
            field=models.ForeignKey(to='torneo.Squadra', related_name='partite2'),
            preserve_default=True,
        ),
    ]
