# Generated by Django 3.1.1 on 2020-09-28 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0015_auto_20200925_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametervalue',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
    ]