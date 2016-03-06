# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0003_auto_20160306_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partita',
            name='campionato',
            field=models.BooleanField(default=True, verbose_name=b'Partita di campionato'),
            preserve_default=True,
        ),
    ]
