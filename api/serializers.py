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
        fields=('id', 'street_name', 'street_number', 'zip_code', 'city_id', 'group_id')

class RawProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=RawProject
        fields=('id', 'name', 'problem', 'solution', 'group_id')

class RawSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=RawSchool
        fields=('id', 'name', 'address', 'principal_name', 'group_id')

class ContestWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContestWinner
        fields=('id', 'contest_id', 'group_id')

class ContestFinalistSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContestFinalist
        fields=('id', 'contest_id', 'group_id')

class GroupRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupRole
        fields=('id', 'group_role_choices', 'user_id', 'group_id')

class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupPost
        fields=('id', 'body', 'title', 'group_role_id', 'group_id')

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostComment
        fields=('id', 'body', 'group_role_id', 'group_post_id')

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostAttachment
        fields=('id', 'group_post_id')

class GroupTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupToken
        fields=('id', 'group_role_choices', 'is_active', 'max_uses', 'group_id')

class TokenUsesSerializer(serializers.ModelSerializer):
    class Meta:
        model=TokenUses
        fields=('id', 'group_token_id', 'user_id')

class RawParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model=RawParticipant
        fields=('id', 'first_name', 'last_name', 'dni', 'email', 'phone_number', 'grade_choices', 'divition_choices', 'group_id')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('id', 'name', 'description')

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectCategory
        fields=('id', 'raw_project_id', 'category')

class GroupSerializer(serializers.ModelSerializer):
    group_location = GroupLocationSerializer()
    raw_participant = RawParticipantSerializer()
    raw_school = RawSchoolSerializer()
    raw_project = RawProjectSerializer()

    class Meta:
        model=Group
        fields=('id', 'name', 'contest_id', 'group_location', 'raw_participant', 'raw_school', 'raw_project')