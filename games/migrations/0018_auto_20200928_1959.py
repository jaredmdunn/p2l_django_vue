# Generated by Django 3.1.1 on 2020-09-28 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0017_auto_20200928_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='default_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parameters_as_default', to='games.parametervalue'),
        ),
    ]
