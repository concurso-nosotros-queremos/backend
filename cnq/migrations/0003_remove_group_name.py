# Generated by Django 2.2.1 on 2019-08-07 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnq', '0002_auto_20190807_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='name',
        ),
    ]
