# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-16 19:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.TextField(help_text='Add an appealing description'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(help_text='Min 0, Max 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]