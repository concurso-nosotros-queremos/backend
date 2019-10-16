from cnq.models import *
from rest_framework import serializers
from django.contrib.auth.models import Group as Group_user
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
import random, string

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'is_active', 'name', 'date_from', 'date_to', 'inscription_date_from', 'inscription_date_to',)

class ContestSerializerEnd(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('inscription_date_to',)


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
        if user.has_perm('view_group', group):
            token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))
            group_token = GroupToken.objects.create(user=user, token=token, **validated_data)
            return group_token
        else:
            raise serializers.ValidationError("No tienes permisos para ejecutar esta accion") 

class Token(object):
    def __init__(self, **kwargs):
        for field in ('id', 'token'):
            setattr(self, field, kwargs.get(field, None))

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length = 7)

    def create(self, validated_data):
        token = Token(id=None, **validated_data)
        user = self.context['request'].user
        for group_token in [GroupToken.objects.get(id=token.id) for token in GroupToken.objects.all()]:
            if group_token.token == token.token:
                group = group_token.group
                assign_perm('view_group', user, group)
                raise serializers.ValidationError("Acceso garantizado")
        raise serializers.ValidationError("Acceso denegado")

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

class GroupSerializer(serializers.ModelSerializer):
    raw_school = RawSchoolSerializer()
    raw_project = RawProjectSerializer()
    raw_participant = RawParticipantSerializer(many=True)
    raw_contact = RawContactSerializer()

    class Meta:
        model = Group
        fields = ('raw_school', 'raw_project', 'raw_participant', 'raw_contact')

    def create(self, validated_data):
        raw_school_data = validated_data.pop('raw_school')
        raw_project_data = validated_data.pop('raw_project')
        raw_participant_data = validated_data.pop('raw_participant')
        raw_contact_data = validated_data.pop('raw_contact')
        categories = raw_project_data.pop('category')


        contest = Contest.objects.get(is_active=True)
        user = self.context['request'].user
        group = Group.objects.create(contest=contest, user=user, **validated_data)
        RawSchool.objects.create(group=group, **raw_school_data)
        raw_project = RawProject.objects.create(group=group, **raw_project_data)
        for raw_participant in raw_participant_data:
            RawParticipant.objects.create(group=group, **raw_participant)
        RawContact.objects.create(group=group, **raw_contact_data)
        categories_obj = [Category.objects.get(id=category.id) for category in categories]
        raw_project.category.set(categories_obj)
        b = User.objects.get(id=4)
        assign_perm('view_group', user, group)
        return group

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
        raw_participant_data = validated_data.pop('raw_participant')
        participants = (instance.raw_participant).all()
        participants = list(participants)
        for participant_data in raw_participant_data:
            participant = participants.pop(0)
            participant.first_name = participant_data.get('first_name', participant.first_name)
            participant.last_name = participant_data.get('last_name', participant.last_name)
            participant.dni = participant_data.get('dni', participant.dni)
            participant.grade_choices = participant_data.get('grade_choices', participant.grade_choices)
            participant.save()

        #Raw_contact
        raw_contact_data = validated_data.pop('raw_contact')
        instance.raw_contact.phone_number = raw_contact_data.pop('phone_number', instance.raw_contact.phone_number)
        instance.raw_contact.alternative_email = raw_contact_data.pop('alternative_email', instance.raw_contact.alternative_email)
        instance.raw_contact.alternative_phone_number = raw_contact_data.pop('alternative_phone_number', instance.raw_contact.alternative_phone_number)
        instance.raw_contact.save()

        return instance
