# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('torneo', '0004_squadra_immagine'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadra',
            name='owner',
            field=models.ForeignKey(related_name='squadre', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
