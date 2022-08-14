# Generated by Django 4.1 on 2022-08-14 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_rename_title_pagecategory_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pagecategory",
            name="game",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="categories",
                to="core.game",
            ),
        ),
    ]