# Generated by Django 2.1.3 on 2018-11-14 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='machine_specs',
        ),
        migrations.AddField(
            model_name='entry',
            name='disk_storage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='entry',
            name='memory',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='entry',
            name='os_version',
            field=models.CharField(default='Not Available', max_length=100),
        ),
        migrations.AddField(
            model_name='entry',
            name='package_versions',
            field=models.TextField(default='Not Available'),
        ),
        migrations.AddField(
            model_name='entry',
            name='processor',
            field=models.CharField(default='Not Available', max_length=100),
        ),
        migrations.AlterField(
            model_name='entry',
            name='command',
            field=models.CharField(default='Not Available', max_length=400),
        ),
        migrations.AlterField(
            model_name='entry',
            name='runtime',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='workload_model',
            field=models.CharField(default='Not Available', max_length=100),
        ),
        migrations.AlterField(
            model_name='entry',
            name='workload_name',
            field=models.CharField(default='Not Available', max_length=100),
        ),
    ]
