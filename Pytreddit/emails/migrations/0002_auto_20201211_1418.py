# Generated by Django 3.1.4 on 2020-12-11 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='from_user',
            field=models.IntegerField(),
        ),
    ]
