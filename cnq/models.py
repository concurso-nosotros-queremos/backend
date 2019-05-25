import datetime
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Contest(models.Model):
    is_active = models.BooleanField('Vigente', default=False)
    year = models.IntegerField('Año', default=datetime.datetime.now().year)
    name = models.CharField('Nombre del concurso', max_length=50)
    date_from = models.DateTimeField('Desde', auto_now_add=True, blank=True)
    date_to = models.DateTimeField('Hasta')

    def __str__(self):
        return 'Edicion: {}'.format(self.year)

class State(models.Model):
    name = models.CharField('Nombre', max_length=10)

    def __str__(self):
        return 'Estado: {}'.format(self.name)

class City(models.Model):
    name = models.CharField('Nombre', max_length=10)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE, related_name='fk_stateCity')

    def __str__(self):
        return 'Ciudad: {}'.format(self.name)


class Group(models.Model):
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='fk_contestGroup')
    

    def __str__(self):
        return 'Concurso: {}'.format(self.contest_id.name)

class GroupLocation(models.Model):
    street_name = models.CharField('Direccion', max_length=20)
    street_number = models.CharField('Altura', max_length=10, default=0)
    zip_code = models.PositiveIntegerField('Zip', validators=[MaxValueValidator(10000), MinValueValidator(0)])
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, related_name='fk_cityGrouplocation')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='fk_groupGroupLocation')

    def __str__(self):
        return '{} {}'.format(self.street_name, self.street_number)

class RawProject(models.Model):
    name = models.CharField('Nombre', max_length=20)
    problem = models.CharField('Problema', max_length=50)
    solution = models.CharField('Solucion', max_length=50)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='fk_groupRawProject')

    def __str__(self):
        return 'Proyecto: {}'.format(self.name)

class RawSchool(models.Model):
    name = models.CharField('Nombre', max_length=10)
    address = models.CharField('Direccion', max_length=20)
    principal_name = models.CharField('Nombre del director', max_length=10)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='fk_groupRawSchool')
    
    def __str__(self):
        return 'Escuela: {}, con su ubicacion en {}'.format(self.name, self.address)


class ContestWinner(models.Model):
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='fk_contestContestWinner')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return 'El proyecto {} gano el concurso {}'.format(self.group_id.fk_groupRawProject, self.contest_id.name)

class ContestFinalist(models.Model):
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='fk_contestContestFinalist')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'El proyecto {} es finalista del concurso {}'.format(self.group_id.fk_groupRawProject, self.contest_id.name)

group_role_choices = [
    (0, 'Anonimo'),
    (1, 'Participant'),
    (2, 'Tutor'),
    (3, 'Mentor'),
]

class GroupRole(models.Model):
    group_role_choices = models.CharField('Rol', max_length=1, choices=group_role_choices, default=0)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fk_userGroupRole')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='fk_groupGroupRole')

    def __str__(self):
        return 'El usuario {} tiene el rol {} para el grupo {}'.format(self.user_id, self.group_role_choices, self.group_id)

class GroupPost(models.Model):
    body = models.CharField('Cuerpo', max_length=50)
    title = models.CharField('Titulo', max_length=15)
    group_role_id = models.ForeignKey(GroupRole, on_delete=models.CASCADE, related_name='fk_grouproleGroupPost')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return 'Titulo: {}, Cuerpo: {}, Grupo: {}'.format(self.title, self.body, self.group_id)

class PostComment(models.Model):
    body = models.CharField('Cuerpo', max_length=50)
    group_role_id = models.ForeignKey(GroupRole, on_delete=models.CASCADE, related_name='fk_grouprolePostComment')
    group_post_id = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='fk_grouppostPostComment')

    def __str__(self):
        return 'Cuerpo: {}, Post: {}'.format(self.body, self.group_post_id)

class PostAttachment(models.Model):
    group_post_id = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='fk_grouppostPostAttachment')
    ##file_url = ??
    ##file_type_choices = ??

    def __str__(self):
        return 'Post: {}'.format(self.group_post_id)


class GroupToken(models.Model):
    group_role_choices = models.CharField('Rol', max_length=1, choices=group_role_choices, default=0)
    ##token = token
    is_active = models.BooleanField('Activo', default=True)
    max_uses = models.IntegerField('Usos maximos', null=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='fk_groupGroupToken')

    def __str__(self):
        return 'Token del grupo {}'.format(self.group_id)

class TokenUses(models.Model):
    group_token_id = models.ForeignKey(GroupToken, on_delete=models.CASCADE, related_name='fk_grouptokenTokenUses')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fk_userTokenUses')

    def __str__(self):
        return 'Usuario: {}, Token: {}'.format(self.user_id, self.group_token_id)

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
    first_name = models.CharField('Nombre', max_length=10)
    last_name = models.CharField('Apellido', max_length=10)
    dni = models.CharField('Dni', max_length=10)
    email = models.EmailField(max_length=20, null= False, unique= True)
    phone_number = models.CharField('Telefono', max_length=30)
    grade_choices = models.CharField(max_length=1, choices=grade_choices)
    divition_choices = models.CharField(max_length=1, choices=divition_choices)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='fk_groupRawParticipant')

    def __str__(self):
        return '{} {}, Dni Nº: {}'.format(self.first_name, self.last_name, self.dni)

class Category(models.Model):
    name = models.CharField('Nombre', max_length=15)
    description = models.CharField('Descripcion', max_length=40)

    def __str__(self):
        return '{}'.format(self.name)

class ProjectCategory(models.Model):
    raw_project_id = models.ForeignKey(RawProject, on_delete=models.CASCADE, related_name='fk_rawprojectProjectcategory')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fk_categoryProjectCategory')

    def __str__(self):
        return '{}, categoria: '.format(self.raw_project_id.name, self.category)

