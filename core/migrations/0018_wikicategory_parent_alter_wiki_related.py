# Generated by Django 4.0.4 on 2022-06-02 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_wiki_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikicategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_cat', to='core.wikicategory'),
        ),
        migrations.AlterField(
            model_name='wiki',
            name='related',
            field=models.ManyToManyField(blank=True, to='core.wiki'),
        ),
    ]