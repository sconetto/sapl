# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-25 21:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materia', '0045_auto_20160823_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
