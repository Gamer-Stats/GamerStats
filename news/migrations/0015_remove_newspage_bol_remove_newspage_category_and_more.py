# Generated by Django 4.0.6 on 2022-07-19 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('profiles', '0019_remove_newsindexpage_page_ptr_and_more'),
        ('news', '0014_newspage_bol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspage',
            name='bol',
        ),
        migrations.RemoveField(
            model_name='newspage',
            name='category',
        ),
        migrations.AddField(
            model_name='newspage',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_news', to='wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='newspage',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_news', to='profiles.profilepage'),
        ),
        migrations.AddField(
            model_name='newspage',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_news', to='profiles.teampage'),
        ),
        migrations.DeleteModel(
            name='NewsCats',
        ),
    ]