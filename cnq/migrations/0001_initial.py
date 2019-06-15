# Generated by Django 2.2.1 on 2019-06-15 04:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='Nombre')),
                ('description', models.CharField(max_length=40, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Vigente')),
                ('year', models.IntegerField(default=2019, verbose_name='Año')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre del concurso')),
                ('date_from', models.DateTimeField(auto_now_add=True, verbose_name='Desde')),
                ('date_to', models.DateTimeField(verbose_name='Hasta')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='Nombre')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='cnq.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=50, verbose_name='Cuerpo')),
                ('title', models.CharField(max_length=15, verbose_name='Titulo')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_post', to='cnq.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_role_choices', models.IntegerField(choices=[(0, 'Anonimo'), (1, 'Participant'), (2, 'Tutor'), (3, 'Mentor')], default=0, verbose_name='Rol')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_role', to='cnq.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_role', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_role_choices', models.IntegerField(choices=[(0, 'Anonimo'), (1, 'Participant'), (2, 'Tutor'), (3, 'Mentor')], default=0, verbose_name='Rol')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('max_uses', models.IntegerField(null=True, verbose_name='Usos maximos')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_token', to='cnq.Group')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='TokenUses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_uses', to='cnq.GroupToken')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_uses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RawSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Nombre')),
                ('address', models.CharField(max_length=20, verbose_name='Direccion')),
                ('principal_name', models.CharField(max_length=10, verbose_name='Nombre del director')),
                ('school_types', models.IntegerField(choices=[(0, 'Publica'), (1, 'Privada'), (2, 'Tecnica Publica'), (3, 'Tecnica Privada'), (4, 'Escuela Rural'), (5, 'Residencia'), (6, 'Tecnica Privada')], default=0, verbose_name='Tipo de escuela')),
                ('com_preference', models.IntegerField(choices=[(0, 'Telefonica'), (1, 'Email'), (2, 'Otro')], default=0, verbose_name='Preferencia de la comunicacion')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_school', to='cnq.Group')),
            ],
        ),
        migrations.CreateModel(
            name='RawProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nombre')),
                ('problem', models.CharField(max_length=50, verbose_name='Problema')),
                ('solution', models.CharField(max_length=50, verbose_name='Solucion')),
                ('diffusion', models.IntegerField(choices=[(0, 'Mail'), (1, 'Afiches del concurso'), (2, 'Redes Sociales'), (3, 'Medios de comunicacion tradicionales'), (4, 'He participado en años anteriores')], default=3, verbose_name='Difusion')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_project', to='cnq.Group')),
            ],
        ),
        migrations.CreateModel(
            name='RawParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=10, verbose_name='Apellido')),
                ('dni', models.CharField(max_length=10, verbose_name='Dni')),
                ('email', models.EmailField(max_length=20, unique=True, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=30, verbose_name='Telefono')),
                ('grade_choices', models.IntegerField(choices=[(0, '4to'), (1, '5to'), (2, '6to'), (3, '7mo')], default=0, verbose_name='Año')),
                ('divition_choices', models.IntegerField(choices=[(0, 'A'), (1, 'B'), (2, 'C')], default=0, verbose_name='Division')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_participant', to='cnq.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_category', to='cnq.Category')),
                ('raw_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_category', to='cnq.RawProject')),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=50, verbose_name='Cuerpo')),
                ('group_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='cnq.GroupPost')),
                ('group_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='cnq.GroupRole')),
            ],
        ),
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_attachment', to='cnq.GroupPost')),
            ],
        ),
        migrations.AddField(
            model_name='grouppost',
            name='group_role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_post', to='cnq.GroupRole'),
        ),
        migrations.CreateModel(
            name='GroupLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(max_length=20, verbose_name='Direccion')),
                ('street_number', models.CharField(default=0, max_length=10, verbose_name='Altura')),
                ('zip_code', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(0)], verbose_name='Zip')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_location', to='cnq.City')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_location', to='cnq.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ContestWinner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_winner', to='cnq.Contest')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_winner', to='cnq.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ContestFinalist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_finalist', to='cnq.Contest')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_finalist', to='cnq.Group')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='cnq.State'),
        ),
    ]
