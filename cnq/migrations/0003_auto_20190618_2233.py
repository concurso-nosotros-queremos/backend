# Generated by Django 2.2.1 on 2019-06-18 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnq', '0002_auto_20190618_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='is_active',
            field=models.BooleanField(default=False, unique=True, verbose_name='Vigente'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Nombre del concurso'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='grouplocation',
            name='street_name',
            field=models.CharField(max_length=35, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='grouplocation',
            name='street_number',
            field=models.CharField(max_length=10, verbose_name='Altura'),
        ),
        migrations.AlterField(
            model_name='grouppost',
            name='body',
            field=models.CharField(max_length=70, verbose_name='Cuerpo'),
        ),
        migrations.AlterField(
            model_name='grouppost',
            name='title',
            field=models.CharField(max_length=20, verbose_name='Titulo'),
        ),
        migrations.AlterField(
            model_name='rawparticipant',
            name='divition_choices',
            field=models.IntegerField(choices=[(0, 'A'), (1, 'B'), (2, 'C')], verbose_name='Division'),
        ),
        migrations.AlterField(
            model_name='rawparticipant',
            name='dni',
            field=models.CharField(max_length=12, unique=True, verbose_name='Dni'),
        ),
        migrations.AlterField(
            model_name='rawparticipant',
            name='email',
            field=models.EmailField(max_length=30, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='rawparticipant',
            name='first_name',
            field=models.CharField(max_length=15, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='rawparticipant',
            name='grade_choices',
            field=models.IntegerField(choices=[(0, '4to'), (1, '5to'), (2, '6to'), (3, '7mo')], verbose_name='Año'),
        ),
        migrations.AlterField(
            model_name='rawparticipant',
            name='last_name',
            field=models.CharField(max_length=15, verbose_name='Apellido'),
        ),
        migrations.AlterField(
            model_name='rawproject',
            name='diffusion',
            field=models.IntegerField(choices=[(0, 'Mail'), (1, 'Afiches del concurso'), (2, 'Redes Sociales'), (3, 'Medios de comunicacion tradicionales'), (4, 'He participado en años anteriores')], verbose_name='Difusion'),
        ),
        migrations.AlterField(
            model_name='rawproject',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='rawproject',
            name='problem',
            field=models.CharField(max_length=70, verbose_name='Problema'),
        ),
        migrations.AlterField(
            model_name='rawproject',
            name='solution',
            field=models.CharField(max_length=150, verbose_name='Solucion'),
        ),
        migrations.AlterField(
            model_name='rawschool',
            name='address',
            field=models.CharField(max_length=40, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='rawschool',
            name='com_preference',
            field=models.IntegerField(choices=[(0, 'Telefonica'), (1, 'Email'), (2, 'Otro')], verbose_name='Preferencia de la comunicacion'),
        ),
        migrations.AlterField(
            model_name='rawschool',
            name='name',
            field=models.CharField(max_length=35, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='rawschool',
            name='principal_name',
            field=models.CharField(max_length=25, verbose_name='Nombre del director'),
        ),
        migrations.AlterField(
            model_name='rawschool',
            name='school_types',
            field=models.IntegerField(choices=[(0, 'Publica'), (1, 'Privada'), (2, 'Tecnica Publica'), (3, 'Tecnica Privada'), (4, 'Escuela Rural'), (5, 'Residencia'), (6, 'Tecnica Privada')], verbose_name='Tipo de escuela'),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Nombre'),
        ),
    ]
