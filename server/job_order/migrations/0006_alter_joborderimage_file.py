# Generated by Django 3.2.24 on 2024-03-31 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_order', '0005_auto_20240330_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joborderimage',
            name='file',
            field=models.FileField(upload_to='media/job_order_files/'),
        ),
    ]
