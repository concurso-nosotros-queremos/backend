from cnq.models import *
from rest_framework import serializers
from django.contrib.auth.models import Group as Group_user
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
import random, string
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'is_active', 'name', 'date_from', 'date_to', 'inscription_date_from', 'inscription_date_to',)

class ContestSerializerEnd(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'inscription_date_to',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class StateSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=True)

    class Meta:
        model = State
        fields = ('id', 'name', 'city')

    def create(self, validated_data):
        city_data = validated_data.pop('city')

        state = State.objects.create(**validated_data)
        for city in city_data:
            City.objects.create(state=state, **city)
        return state


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ('id', 'category')


class RawSchoolSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name", read_only=True)
    state_name = serializers.CharField(source="city.state.name", read_only=True)
    school_types_name = serializers.CharField(source="get_school_types_display", read_only=True)

    class Meta:
        model = RawSchool
        fields = ('id', 'name', 'street_name', 'street_number', 'city', 'city_name', 'state_name', 'school_types', 'school_types_name')

class ContestWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestWinner
        fields = ('id', 'contest', 'group')


class ContestFinalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestFinalist
        fields = ('id', 'contest', 'group')


class GroupRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRole
        fields = ('id', 'group_role_choices', 'user', 'group')


class GroupTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupToken
        fields = ('is_active', 'max_uses', 'group')

    def create(self, validated_data):
        user = self.context['request'].user
        group = validated_data.get('group')
        if user.has_perm('view_group', group) or group.user == self.context['request'].user:
            token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))
            group_token = GroupToken.objects.create(user=user, token=token, **validated_data)
            return group_token
        else:
            raise serializers.ValidationError("No tienes permisos para ejecutar esta accion") 
    
    def to_representation(self, instance):
        ret = super(GroupTokenSerializer, self).to_representation(instance)
        # check the request is list view or detail view
        is_list_view = isinstance(self.instance, list)
        extra_ret = {'token': instance.token} if is_list_view else {'token': instance.token}
        ret.update(extra_ret)
        return ret
        
class Token(object):
    def __init__(self, **kwargs):
        for field in ('id', 'token'):
            setattr(self, field, kwargs.get(field, None))

class SuccessAccess(APIException):
    status_code = 200
    default_detail = 'Acceso garantizado'
    default_code = 'success'

class DeniedAccess(APIException):
    status_code = 401
    default_detail = 'Acceso denegado'
    default_code = 'denied'

class AlreadyAccess(APIException):
    status_code = 200
    default_detail = 'Ya tienes accesso'
    default_code = 'success'

class BadRequest(APIException):
    status_code = 400
    default_detail = 'Token incorrecto'
    default_code = 'bad'

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length = 7)

    def create(self, validated_data):
        token = Token(id=None, **validated_data)
        print(token.token)
        user = self.context['request'].user
        for group_token in [Group.objects.get(id=i.id) for i in Group.objects.all()]:
            print(group_token.token)
            if group_token.token == token.token:
                if (user != group_token.user) and (user.has_perm('view_group', group_token) != True):
                    assign_perm('view_group', user, group_token)
                    raise SuccessAccess
                else: 
                    raise AlreadyAccess
        raise BadRequest

class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

class TokenUsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenUses
        fields = ('id', 'group_token_id', 'user')


class RawParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawParticipant
        fields = ('id', 'first_name', 'last_name', 'dni', 'grade_choices')


class RawContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawContact
        fields = ('id', 'phone_number', 'alternative_email', 'alternative_phone_number')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class RawProjectSerializer(serializers.ModelSerializer):
    category_name = CategorySerializer(source="category", many=True, read_only=True)
    diffusion_name = serializers.CharField(source="get_diffusion_display", read_only=True)

    class Meta:
        model = RawProject
        fields = ('id', 'name', 'problem', 'solution', 'diffusion', 'category', 'category_name', 'diffusion_name')



class MessageEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageEmail
        fields = ('name', 'email', 'message', 'date')
    
    def create(self, validated_data):
        memail = MessageEmail.objects.create(**validated_data)
        email = EmailMessage(
            subject='Duda CNQ',
            body= "Nombre: " + validated_data.get('name') + ", Email: " + validated_data.get('email') + ", Mensaje: " + validated_data.get('message'),
            from_email=settings.EMAIL_HOST_USER,
            to=[validated_data.get('email')]
        )
        email.send()
        return memail


class GroupSerializer(serializers.ModelSerializer):
    raw_school = RawSchoolSerializer()
    raw_project = RawProjectSerializer()
    raw_participant = RawParticipantSerializer(many=True)
    raw_contact = RawContactSerializer()

    class Meta:
        model = Group
        fields = ('id', 'raw_school', 'raw_project', 'raw_participant', 'raw_contact')

    def create(self, validated_data):
        raw_school_data = validated_data.pop('raw_school')
        raw_project_data = validated_data.pop('raw_project')
        raw_participant_data = validated_data.pop('raw_participant')
        raw_contact_data = validated_data.pop('raw_contact')
        categories = raw_project_data.pop('category')


        contest = Contest.objects.get(is_active=True)
        user = self.context['request'].user
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))
        group = Group.objects.create(contest=contest, user=user, token=token, **validated_data)
        RawSchool.objects.create(group=group, **raw_school_data)
        raw_project = RawProject.objects.create(group=group, **raw_project_data)
        for raw_participant in raw_participant_data:
            RawParticipant.objects.create(group=group, **raw_participant)
        RawContact.objects.create(group=group, **raw_contact_data)
        categories_obj = [Category.objects.get(id=category.id) for category in categories]
        raw_project.category.set(categories_obj)
        assign_perm('view_group', user, group)
        return group
    
    def to_representation(self, instance):
        ret = super(GroupSerializer, self).to_representation(instance)
        is_list_view = isinstance(self.instance, list)
        extra_ret = {'token': instance.token} if is_list_view else {'token': instance.token}
        ret.update(extra_ret)
        return ret

    def update(self, instance, validated_data):
        #Raw_school
        raw_school_data = validated_data.pop('raw_school')
        instance.raw_school.name = raw_school_data.pop('name', instance.raw_school.name)
        instance.raw_school.street_name = raw_school_data.pop('street_name', instance.raw_school.street_name)
        instance.raw_school.street_number = raw_school_data.pop('street_number', instance.raw_school.street_number)
        instance.raw_school.city = raw_school_data.pop('city', instance.raw_school.city)
        instance.raw_school.school_types = raw_school_data.pop('school_types', instance.raw_school.school_types)
        instance.raw_school.save()

        #Raw_project
        raw_project_data = validated_data.pop('raw_project')
        instance.raw_project.name = raw_project_data.pop('name', instance.raw_project.name)
        instance.raw_project.problem = raw_project_data.pop('problem', instance.raw_project.problem)
        instance.raw_project.solution = raw_project_data.pop('solution', instance.raw_project.solution)
        instance.raw_project.diffusion = raw_project_data.pop('diffusion', instance.raw_project.diffusion)
        categories_obj = [Category.objects.get(id=category.id) for category in raw_project_data.pop('category', instance.raw_project.category.all())]
        instance.raw_project.category.set(categories_obj)
        instance.raw_project.save()

        #Raw_participant
        print(instance.id)
        raw_participants = RawParticipant.objects.filter(group=instance.id)
        raw_participants.delete()
        raw_participant_data = validated_data.pop('raw_participant')

        for raw_participant in raw_participant_data:
            RawParticipant.objects.create(group=instance, **raw_participant)



        #Raw_contact
        raw_contact_data = validated_data.pop('raw_contact')
        instance.raw_contact.phone_number = raw_contact_data.pop('phone_number', instance.raw_contact.phone_number)
        instance.raw_contact.alternative_email = raw_contact_data.pop('alternative_email', instance.raw_contact.alternative_email)
        instance.raw_contact.alternative_phone_number = raw_contact_data.pop('alternative_phone_number', instance.raw_contact.alternative_phone_number)
        instance.raw_contact.save()

        return instance
