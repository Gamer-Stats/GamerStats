# Generated by Django 4.0.6 on 2022-07-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profilepage_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepage',
            name='player_rank',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
