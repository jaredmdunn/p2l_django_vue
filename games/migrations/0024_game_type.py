# Generated by Django 3.1.1 on 2020-10-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0023_auto_20201002_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Vanilla'), (2, 'Vue')], default=1),
        ),
    ]
