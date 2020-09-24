# Generated by Django 3.1.1 on 2020-09-24 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_auto_20200924_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='parameter',
            name='values',
        ),
        migrations.AddField(
            model_name='parameter',
            name='parameter_values',
            field=models.ManyToManyField(related_name='parameters', to='games.ParameterValue'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='default_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters_as_default', to='games.parametervalue'),
        ),
    ]
