# Generated by Django 3.1.5 on 2021-03-21 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_merchant_merchantkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='txntype',
            field=models.TextField(blank=True, null=True),
        ),
    ]