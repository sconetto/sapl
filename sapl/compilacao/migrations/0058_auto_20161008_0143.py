# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-08 04:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compilacao', '0057_auto_20161007_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispositivo',
            name='ta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dispositivos_set', to='compilacao.TextoArticulado', verbose_name='Texto Articulado'),
        ),
        migrations.AlterField(
            model_name='dispositivo',
            name='ta_publicado',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dispositivos_alterados_pelo_ta_set', to='compilacao.TextoArticulado', verbose_name='Texto Articulado Publicado'),
        ),
        migrations.AlterField(
            model_name='dispositivo',
            name='tipo_dispositivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dispositivos_do_tipo_set', to='compilacao.TipoDispositivo', verbose_name='Tipo do Dispositivo'),
        ),
    ]
