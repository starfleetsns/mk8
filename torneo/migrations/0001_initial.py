# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Partita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('punteggio11', models.IntegerField(default=0, verbose_name=b'Prima squadra, primo giocatore')),
                ('punteggio12', models.IntegerField(default=0, verbose_name=b'Prima squadra, secondo giocatore')),
                ('punteggio21', models.IntegerField(default=0, verbose_name=b'Seconda squadra, primo giocatore')),
                ('punteggio22', models.IntegerField(default=0, verbose_name=b'Seconda squadra, secondo giocatore')),
                ('stato', models.CharField(default=b'INC', max_length=3, choices=[(b'INC', b'Partita non disputata'), (b'AT1', b'In attesa di conferma dalla prima squadra'), (b'AT2', b'In attesa di conferma della seconda squadra'), (b'DON', b'Punteggio confermato')])),
                ('data', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreferenzeUtente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iscritto', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='preferenze', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Squadra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200, verbose_name=b'Nome della squadra')),
                ('punteggio', models.IntegerField(default=0)),
                ('lunghezza', models.IntegerField(default=0)),
                ('immagine', models.ImageField(default=b'torneo/squadra/default.png', upload_to=b'torneo/squadra')),
                ('confermata', models.BooleanField(default=False)),
                ('giocatore1', models.ForeignKey(related_name='squadre1', verbose_name=b'Primo giocatore', to=settings.AUTH_USER_MODEL)),
                ('giocatore2', models.ForeignKey(related_name='squadre2', verbose_name=b'Secondo giocatore', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='partita',
            name='squadra1',
            field=models.ForeignKey(related_name='partite1', verbose_name=b'Prima squadra', to='torneo.Squadra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partita',
            name='squadra2',
            field=models.ForeignKey(related_name='partite2', verbose_name=b'Seconda squadra', to='torneo.Squadra'),
            preserve_default=True,
        ),
    ]
