# Generated by Django 3.0.3 on 2020-03-03 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0002_auto_20200302_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='some_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
