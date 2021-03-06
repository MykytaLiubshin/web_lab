# Generated by Django 3.1.4 on 2020-12-11 14:02

import django.contrib.postgres.fields
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0006_auto_20201210_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('photo', models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to='')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('contents_files', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to=''), blank=True, default=list, size=None)),
                ('from_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('reply_to', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emails.letter')),
            ],
        ),
        migrations.CreateModel(
            name='ForumMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('contents_files', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to=''), blank=True, default=list, size=None)),
                ('from_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('reply_to', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emails.forummessage')),
                ('to_forum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='emails.forum')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('contents_files', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to=''), blank=True, default=list, size=None)),
                ('to_user', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('subject', models.CharField(max_length=1000, null=True)),
                ('from_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('reply_to', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emails.email')),
            ],
        ),
    ]
