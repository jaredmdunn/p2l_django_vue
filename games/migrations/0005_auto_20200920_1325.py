# Generated by Django 3.1.1 on 2020-09-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_game_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
    ]
