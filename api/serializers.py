from cnq.models import *
from rest_framework import serializers
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin
from django.contrib.auth.models import Group as Group_user
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'is_active', 'name', 'date_from', 'date_to', 'inscription_date_from', 'inscription_date_to')


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


class RawProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawProject
        fields = ('id', 'name', 'problem', 'solution', 'diffusion', 'category')


class RawSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawSchool
        fields = ('id', 'name', 'street_name', 'street_number', 'city', 'school_types')


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
        fields = ('id', 'group_role_choices', 'is_active', 'max_uses', 'group')


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
        a = User.objects.get(id=2)
        b = User.objects.get(id=3)
        assign_perm('view_group', a, group)
        assign_perm('view_group', b, group)
        return group