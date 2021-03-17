# Generated by Django 3.1.5 on 2021-03-17 12:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paycode', models.TextField()),
                ('token', models.CharField(max_length=100)),
                ('datetime', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'pay_token',
            },
        ),
    ]
