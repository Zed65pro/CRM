# Generated by Django 3.2.24 on 2024-03-30 13:00

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_order', '0002_joborder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joborder',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=django.contrib.gis.geos.point.Point(35.2154, 31.8974), srid=4326),
        ),
        migrations.AlterField(
            model_name='joborder',
            name='name',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]