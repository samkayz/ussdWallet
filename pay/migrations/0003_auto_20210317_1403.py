# Generated by Django 3.1.5 on 2021-03-17 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0002_auto_20210317_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paytoken',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]