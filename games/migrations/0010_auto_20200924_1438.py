# Generated by Django 3.1.1 on 2020-09-24 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_auto_20200923_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['game']},
        ),
    ]
