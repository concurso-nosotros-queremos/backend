from cnq.models import *
from rest_framework import serializers

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contest
        fields=('id', 'is_active', 'year', 'name', 'date_from', 'date_to')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model=State
        fields=('id', 'name')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields=('id', 'name')

class GroupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupLocation
        fields=('id', 'street_name', 'street_number', 'zip_code', 'city')

class RawProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=RawProject
        fields=('id', 'name', 'problem', 'solution', 'diffusion')

class RawSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=RawSchool
        fields=('id', 'name', 'address', 'principal_name', 'school_types', 'com_preference')

class ContestWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContestWinner
        fields=('id', 'contest', 'group')

class ContestFinalistSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContestFinalist
        fields=('id', 'contest', 'group')

class GroupRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupRole
        fields=('id', 'group_role_choices', 'user', 'group')

class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupPost
        fields=('id', 'body', 'title', 'group_role', 'group')

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostComment
        fields=('id', 'body', 'group_role', 'group_post')

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostAttachment
        fields=('id', 'group_post')

class GroupTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupToken
        fields=('id', 'group_role_choices', 'is_active', 'max_uses', 'group')

class TokenUsesSerializer(serializers.ModelSerializer):
    class Meta:
        model=TokenUses
        fields=('id', 'group_token_id', 'user')

class RawParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model=RawParticipant
        fields=('id', 'first_name', 'last_name', 'dni', 'email', 'phone_number', 'grade_choices', 'divition_choices')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('id', 'name', 'description')

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectCategory
        fields=('id', 'raw_project_id', 'category')

class GroupSerializer(serializers.ModelSerializer):
    group_location = GroupLocationSerializer(many=True)
    raw_participant = RawParticipantSerializer(many=True)
    raw_school = RawSchoolSerializer(many=True)
    raw_project = RawProjectSerializer(many=True)
    class Meta:
        model=Group
        fields=('__all__')

    def create(self, validated_data):
        group_location_data = validated_data.pop('group_location')
        raw_participant_data = validated_data.pop('raw_participant')
        raw_school_data = validated_data.pop('raw_school')
        raw_project_data = validated_data.pop('raw_project')
        group = Group.objects.create(**validated_data)
        for group_location in group_location_data:
            GroupLocation.objects.create(group=group, **group_location)
        for raw_participant in raw_participant_data:
            RawParticipant.objects.create(group=group, **raw_participant)
        for raw_school in raw_school_data:
            RawSchool.objects.create(group=group, **raw_school)
        for raw_project in raw_project_data:
            RawProject.objects.create(group=group, **raw_project)
        return group