# Generated by Django 3.2.24 on 2024-03-30 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_order', '0004_auto_20240330_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joborder',
            name='images',
        ),
        migrations.AlterField(
            model_name='joborderimage',
            name='job_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='job_order.joborder'),
        ),
    ]