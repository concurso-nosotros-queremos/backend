# Generated by Django 2.2.1 on 2019-06-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnq', '0002_auto_20190612_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='name',
            field=models.CharField(default='Hola', max_length=15, verbose_name='Nombre'),
        ),
    ]
