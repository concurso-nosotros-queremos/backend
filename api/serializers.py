from cnq.models import *
from rest_framework import serializers


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'is_active', 'year', 'name', 'date_from', 'date_to', 'inscription_date_from', 'inscription_date_to')


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


class GroupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupLocation
        fields = ('id', 'street_name', 'street_number', 'zip_code', 'city')


class RawProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawProject
        fields = ('id', 'name', 'problem', 'solution', 'diffusion')


class RawSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawSchool
        fields = ('id', 'name', 'address', 'principal_name', 'school_types', 'com_preference')


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


class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPost
        fields = ('id', 'body', 'title', 'group_role', 'group')


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ('id', 'body', 'group_role', 'group_post')


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'group_post')


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
        fields = ('id', 'first_name', 'last_name', 'dni', 'email', 'phone_number', 'grade_choices', 'divition_choices')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ('id', 'raw_project_id', 'category')


class GroupSerializer(serializers.ModelSerializer):
    group_location = GroupLocationSerializer()
    raw_school = RawSchoolSerializer()
    raw_project = RawProjectSerializer()
    raw_participant = RawParticipantSerializer(many=True)

    class Meta:
        model = Group
        fields = ('group_location', 'raw_school', 'raw_project', 'raw_participant', 'name')

    def create(self, validated_data):
        group_location_data = validated_data.pop('group_location')
        raw_school_data = validated_data.pop('raw_school')
        raw_project_data = validated_data.pop('raw_project')
        raw_participant_data = validated_data.pop('raw_participant')

        contest = Contest.objects.get(is_active=True)
        group = Group.objects.create(contest=contest, **validated_data)
        GroupLocation.objects.create(group=group, **group_location_data)
        RawSchool.objects.create(group=group, **raw_school_data)
        RawProject.objects.create(group=group, **raw_project_data)
        for raw_participant in raw_participant_data:
            RawParticipant.objects.create(group=group, **raw_participant)
        return group
