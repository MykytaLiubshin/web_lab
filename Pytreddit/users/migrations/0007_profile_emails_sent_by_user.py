# Generated by Django 3.1.4 on 2020-12-11 14:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201210_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='emails_sent_by_user',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None),
        ),
    ]
