# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-15 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20160701_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentos_administrativos', models.CharField(blank=True, choices=[('O', 'Ostensivo'), ('R', 'Restritivo')], max_length=1, null=True, verbose_name='Ostensivo/Restritivo')),
                ('sequencia_numeracao', models.CharField(blank=True, choices=[('A', 'Sequencial por ano'), ('U', 'Sequencial único')], max_length=1, null=True, verbose_name='Sequência de numeração')),
                ('painel_aberto', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], verbose_name='Painel aberto para usuário anônimo')),
            ],
        ),
    ]
