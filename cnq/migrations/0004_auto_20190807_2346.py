# Generated by Django 2.2.1 on 2019-08-07 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cnq', '0003_remove_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawcontact',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='raw_contact', to='cnq.Group'),
        ),
    ]
