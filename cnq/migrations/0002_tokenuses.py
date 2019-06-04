# Generated by Django 2.2.1 on 2019-05-25 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cnq', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenUses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_token_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_grouptokenTokenUses', to='cnq.GroupToken')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_userTokenUses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]