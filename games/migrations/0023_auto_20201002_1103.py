# Generated by Django 3.1.1 on 2020-10-02 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0022_merge_20201001_1544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parametervalue',
            options={'ordering': ['parameter', 'ordering_name']},
        ),
    ]
