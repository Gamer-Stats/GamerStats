# Generated by Django 4.0.4 on 2022-06-06 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('slug', models.SlugField(blank=True, max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('meta_title', models.CharField(blank=True, max_length=70)),
                ('meta_description', models.TextField(blank=True)),
                ('canonical_url', models.URLField(blank=True, null=True)),
                ('index_page', models.BooleanField(default=True)),
                ('publish', models.BooleanField(default=False)),
                ('active_players', models.ManyToManyField(blank=True, related_name='active_squad', to='core.setupsettings')),
                ('avatar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to='core.imagecollection')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_name', to='core.wiki')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_name', to='core.wiki')),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.DeleteModel(
            name='Stats',
        ),
    ]
