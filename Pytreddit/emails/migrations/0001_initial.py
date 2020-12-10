# Generated by Django 3.1.4 on 2020-12-10 16:58

import django.contrib.postgres.fields
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_auto_20201209_1019'),
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
            name='Email',
            fields=[
                ('letter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='emails.letter')),
                ('to_user', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('subject', models.CharField(max_length=1000)),
            ],
            bases=('emails.letter', models.Model),
        ),
        migrations.CreateModel(
            name='ForumMessage',
            fields=[
                ('letter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='emails.letter')),
                ('to_forum', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='emails.forum')),
            ],
            bases=('emails.letter', models.Model),
        ),
    ]
