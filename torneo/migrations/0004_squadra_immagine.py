# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0003_squadra_punteggio'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadra',
            name='immagine',
            field=models.ImageField(default=b'torneo/squadra/default.png', upload_to=b'torneo/squadra'),
            preserve_default=True,
        ),
    ]
