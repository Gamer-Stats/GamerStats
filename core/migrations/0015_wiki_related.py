# Generated by Django 4.0.4 on 2022-06-01 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_news_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiki',
            name='related',
            field=models.ManyToManyField(blank=True, null=True, to='core.wiki'),
        ),
    ]