# Generated by Django 2.2.1 on 2019-06-29 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnq', '0004_auto_20190619_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=60, unique=True, verbose_name='Nombre'),
        ),
    ]
