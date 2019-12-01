import datetime
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from datetime import datetime
from django.db import DataError
# Create your models here.

class MessageEmail(models.Model):
    name = models.CharField('Nombre', max_length=30, null=False)
    email = models.EmailField('Email', max_length=50, null=False)
    message = models.CharField('Mensaje', max_length=240, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return 'Nombre: {}, Email: {}, Fecha: {}'.format(self.name, self.email, self.date)
    
class Contest(models.Model):
    is_active = models.BooleanField('Vigente', default=False)
    name = models.CharField('Nombre del concurso', max_length=30, null=False)
    date_from = models.DateTimeField('Desde', null=False)
    date_to = models.DateTimeField('Hasta', null=False)
    inscription_date_from = models.DateTimeField('Inscripcion desde', null=False)
    inscription_date_to = models.DateTimeField('Inscripcion_hasta', null=False)

    def save(self, *args, **kwargs):
        if Contest.objects.filter(is_active=True).exclude(id=self.id):
            if self.is_active is True:
                raise DataError('No se puede tener mas de un grupo activo en simultaneo')
        super(Contest, self).save(*args, **kwargs)

    def __str__(self):
        return 'Nombre: {}'.format(self.name)


class State(models.Model):
    name = models.CharField('Nombre', max_length=20, null=False, unique=True)

    def __str__(self):
        return 'Estado: {}'.format(self.name)


class City(models.Model):
    name = models.CharField('Nombre', max_length=60, null=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='city')
    class Meta:
        unique_together = ('name', 'state',)
    
    def __str__(self):
        return 'Ciudad: {}'.format(self.name)


class Group(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='group')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1')
    def __str__(self):
        return 'Concurso: {}'.format(self.contest.name)



class Category(models.Model):
    name = models.CharField('Nombre', max_length=30, null=False)
    description = models.CharField('Descripcion', max_length=300)

    def __str__(self):
        return '{}'.format(self.name)


class RawProject(models.Model):
    specialCharacters = RegexValidator(regex='^[a-zA-Z ]*$', message='Caracteres espciales no esta disponibles')
    DIFFUSION = [
        (0, 'Mail'),
        (1, 'Afiches del concurso'),
        (2, 'Redes Sociales'),
        (3, 'Medios de comunicacion tradicionales'),
        (4, 'He participado en años anteriores'),
    ]

    name = models.CharField('Nombre', max_length=50, null=False)
    problem = models.CharField('Problema', max_length=500, null=False)
    solution = models.CharField('Solucion', max_length=500, null=False)
    diffusion = models.PositiveIntegerField('Difusion', choices=DIFFUSION, null=False, validators=[MaxValueValidator(4), MinValueValidator(0)])
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='raw_project')
    category = models.ManyToManyField(Category, related_name='raw_project')

    def __str__(self):
        return '{}'.format(self.name)


school_types = [
    (0, 'Publica'),
    (1, 'Privada'),
    (2, 'Tecnica Publica'),
    (3, 'Tecnica Privada'),
    (4, 'Escuela Rural'),
    (5, 'Residencia'),
    ##Others
]

class RawSchool(models.Model):
    specialCharacters = RegexValidator(regex='^[a-zA-Z ]*$', message='Caracteres espciales no esta disponibles')

    name = models.CharField('Nombre', max_length=60, null=False)
    street_name = models.CharField('Direccion', max_length=60)
    street_number = models.PositiveIntegerField('Altura', null=False, validators=[MaxValueValidator(99999)])
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='group_location')
    school_types = models.PositiveIntegerField('Tipo de escuela', choices=school_types, null=False, validators=[MinValueValidator(0)])
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='raw_school')

    def __str__(self):
        return 'Escuela: {}, con su ubicacion en {} al {}'.format(self.name, self.street_name, self.street_number)


class ContestWinner(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='contest_winner')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='contest_winner')

    def __str__(self):
        return 'El grupo {} gano el concurso {}'.format(self.group.name, self.contest.name)


class ContestFinalist(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='contest_finalist')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='contest_finalist')

    def __str__(self):
        return 'El grupo {} es finalista del concurso {}'.format(self.group, self.contest.name)


group_role_choices = [
    (0, 'Anonimo'),
    (1, 'Participant'),
    (2, 'Tutor'),
    (3, 'Mentor'),
]


class GroupRole(models.Model):
    group_role_choices = models.PositiveIntegerField('Rol', choices=group_role_choices, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_role')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_role')

    def __str__(self):
        return 'El usuario {} tiene el rol {} para el grupo {}'.format(self.user, self.group_role_choices, self.group)

class GroupToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    token = models.CharField('Token', max_length=7, null=False, unique=True)
    is_active = models.BooleanField('Activo', default=True)
    max_uses = models.PositiveIntegerField('Usos maximos', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return 'Token del grupo {}'.format(self.group)


class TokenUses(models.Model):
    group_token = models.ForeignKey(GroupToken, on_delete=models.CASCADE, related_name='token_uses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token_uses')

    def __str__(self):
        return 'Usuario: {}, Token: {}'.format(self.user, self.group_token)


grade_choices = [
    (0, '4to'),
    (1, '5to'),
    (2, '6to'),
    (3, '7mo'),
]

class RawParticipant(models.Model):
    specialCharacters = RegexValidator(regex='^[a-zA-Z ]*$', message='Caracteres espciales no esta disponibles')

    first_name = models.CharField('Nombre', max_length=20, null=False)
    last_name = models.CharField('Apellido', max_length=20, null=False)
    dni = models.PositiveIntegerField('Dni', null=False, validators=[MinValueValidator(10000000), MaxValueValidator(99999999)])
    grade_choices = models.PositiveIntegerField('Año', choices=grade_choices, null=False, validators=[MinValueValidator(0)])
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='raw_participant')

    def __str__(self):
        return '{} {}, Dni Nº: {}'.format(self.first_name, self.last_name, self.dni)

class RawContact(models.Model):
    phone_number = models.PositiveIntegerField('Numero del tutor', null=False, validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    alternative_email = models.EmailField('Mail del tutor alternativo', max_length=70, null=False)
    alternative_phone_number = models.PositiveIntegerField('Numero del tutor alternativo', null=False, validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='raw_contact')

    def __str__(self):
        return '{}'.format(self.phone_number)


class ProjectCategory(models.Model):
    raw_project = models.ForeignKey(RawProject, on_delete=models.CASCADE, related_name='raw_project')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='project_category')

    def __str__(self):
        return '{}, categoria: {}'.format(self.raw_project.name, self.category.name)