# Generated by Django 3.1.1 on 2020-09-23 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_remove_parameter_input_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamescore',
            old_name='game_id',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='gamescore',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='gamescoreparameters',
            old_name='gamescore_id',
            new_name='gamescore',
        ),
        migrations.RenameField(
            model_name='gamescoreparameters',
            old_name='parameter_id',
            new_name='parameter',
        ),
        migrations.RenameField(
            model_name='parameter',
            old_name='game_id',
            new_name='game',
        ),
    ]
