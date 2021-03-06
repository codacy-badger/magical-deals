# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-16 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200816_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(help_text='Add an appealing description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='', help_text='Please choose a catchy name', max_length=254),
        ),
    ]
