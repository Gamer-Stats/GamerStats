# Generated by Django 4.0.6 on 2022-07-15 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Post date'),
        ),
        migrations.AlterField(
            model_name='newspage',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Updated date'),
        ),
    ]
