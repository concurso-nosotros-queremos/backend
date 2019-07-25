import datetime
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Contest(models.Model):
    is_active = models.BooleanField('Vigente', default=False)
    name = models.CharField('Nombre del concurso', max_length=30, null=False)
    date_from = models.DateTimeField('Desde', null=False)
    date_to = models.DateTimeField('Hasta', null=False)
    inscription_date_from = models.DateTimeField('Inscripcion desde', null=False)
    inscription_date_to = models.DateTimeField('Inscripcion_hasta', null=False)

    def save(self, *args, **kwargs):
        if Contest.objects.filter(is_active=True):
            if self.is_active is True:
                self.is_active = None
        super(Contest, self).save(*args, **kwargs)

    def __str__(self):
        return 'Edicion: {}'.format(self.year)


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
    name = models.CharField('Nombre', max_length=20, null=False)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return 'Grupo: {}, Concurso: {}'.format(self.name, self.contest.name)


class GroupLocation(models.Model):
    street_name = models.CharField('Direccion', max_length=35, null=False)
    street_number = models.CharField('Altura', max_length=10, null=False)
    zip_code = models.PositiveIntegerField('Zip', validators=[MaxValueValidator(10000), MinValueValidator(0)], null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='group_location')
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='group_location')

    def __str__(self):
        return '{} {}'.format(self.street_name, self.street_number)


diffusion = [
    (0, 'Mail'),
    (1, 'Afiches del concurso'),
    (2, 'Redes Sociales'),
    (3, 'Medios de comunicacion tradicionales'),
    (4, 'He participado en años anteriores'),
]


class RawProject(models.Model):
    name = models.CharField('Nombre', max_length=30, null=False)
    problem = models.CharField('Problema', max_length=70, null=False)
    solution = models.CharField('Solucion', max_length=150, null=False)
    diffusion = models.IntegerField('Difusion', choices=diffusion, null=False)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='raw_project')

    def __str__(self):
        return 'Proyecto: {}'.format(self.name)


school_types = [
    (0, 'Publica'),
    (1, 'Privada'),
    (2, 'Tecnica Publica'),
    (3, 'Tecnica Privada'),
    (4, 'Escuela Rural'),
    (5, 'Residencia'),
    (6, 'Tecnica Privada'),
]

com_preferences = [
    (0, 'Telefonica'),
    (1, 'Email'),
    (2, 'Otro'),
]


class RawSchool(models.Model):
    name = models.CharField('Nombre', max_length=35, null=False)
    address = models.CharField('Direccion', max_length=40)
    principal_name = models.CharField('Nombre del director', max_length=25)
    school_types = models.IntegerField('Tipo de escuela', choices=school_types, null=False)
    com_preference = models.IntegerField('Preferencia de la comunicacion', choices=com_preferences, null=False)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='raw_school')

    def __str__(self):
        return 'Escuela: {}, con su ubicacion en {}'.format(self.name, self.address)


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
    group_role_choices = models.IntegerField('Rol', choices=group_role_choices, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_role')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_role')

    def __str__(self):
        return 'El usuario {} tiene el rol {} para el grupo {}'.format(self.user, self.group_role_choices, self.group)


class GroupPost(models.Model):
    body = models.CharField('Cuerpo', max_length=70)
    title = models.CharField('Titulo', max_length=20)
    group_role = models.ForeignKey(GroupRole, on_delete=models.CASCADE, related_name='group_post')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_post')

    def __str__(self):
        return 'Titulo: {}, Cuerpo: {}, Grupo: {}'.format(self.title, self.body, self.group)


class PostComment(models.Model):
    body = models.CharField('Cuerpo', max_length=50)
    group_role = models.ForeignKey(GroupRole, on_delete=models.CASCADE, related_name='post_comment')
    group_post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='post_comment')

    def __str__(self):
        return 'Cuerpo: {}, Post: {}'.format(self.body, self.group_post)


class PostAttachment(models.Model):
    group_post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='post_attachment')

    ##file_url = ??
    ##file_type_choices = ??

    def __str__(self):
        return 'Post: {}'.format(self.group_post)


class GroupToken(models.Model):
    group_role_choices = models.IntegerField('Rol', choices=group_role_choices, default=0)
    ##token = token
    is_active = models.BooleanField('Activo', default=True)
    max_uses = models.IntegerField('Usos maximos', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_token')

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
divition_choices = [
    (0, 'A'),
    (1, 'B'),
    (2, 'C'),
]


class RawParticipant(models.Model):
    first_name = models.CharField('Nombre', max_length=15, null=False)
    last_name = models.CharField('Apellido', max_length=15, null=False)
    dni = models.CharField('Dni', max_length=12, null=False)
    email = models.EmailField('Email', max_length=30, null=True)
    phone_number = models.CharField('Telefono', null=True, max_length=30)
    grade_choices = models.IntegerField('Año', choices=grade_choices, null=False)
    divition_choices = models.IntegerField('Division', choices=divition_choices, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='raw_participant')

    def __str__(self):
        return '{} {}, Dni Nº: {}'.format(self.first_name, self.last_name, self.dni)


class Category(models.Model):
    name = models.CharField('Nombre', max_length=20, null=False)
    description = models.CharField('Descripcion', max_length=40)

    def __str__(self):
        return '{}'.format(self.name)


class ProjectCategory(models.Model):
    raw_project = models.ForeignKey(RawProject, on_delete=models.CASCADE, related_name='project_category')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='project_category')

    def __str__(self):
        return '{}, categoria: '.format(self.raw_project.name, self.category)
