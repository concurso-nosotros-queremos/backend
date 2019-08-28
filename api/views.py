from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from cnq.models import *
from rest_framework.permissions import IsAuthenticated
from itertools import chain


# Create your views here.
class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        user = self.request.user
        if user.is_staff == 1:
            group = Group.objects.all()
        else:
            group = Group.objects.filter(user=user) | Group.objects.filter(user2=user)
        return group


class RawProjectViewSet(viewsets.ModelViewSet):
    queryset = RawProject.objects.all()
    serializer_class = RawProjectSerializer


class RawSchoolViewSet(viewsets.ModelViewSet):
    queryset = RawSchool.objects.all()
    serializer_class = RawSchoolSerializer


class ContestWinnerViewSet(viewsets.ModelViewSet):
    queryset = ContestWinner.objects.all()
    serializer_class = ContestWinnerSerializer


class ContestFinalistViewSet(viewsets.ModelViewSet):
    queryset = ContestFinalist.objects.all()
    serializer_class = ContestFinalistSerializer


class GroupRoleViewSet(viewsets.ModelViewSet):
    queryset = GroupRole.objects.all()
    serializer_class = GroupRoleSerializer


class GroupTokenViewSet(viewsets.ModelViewSet):
    queryset = GroupToken.objects.all()
    serializer_class = GroupTokenSerializer


class TokenUsesViewSet(viewsets.ModelViewSet):
    queryset = TokenUses.objects.all()
    serializer_class = TokenUsesSerializer


class RawParticipantViewSet(viewsets.ModelViewSet):
    queryset = RawParticipant.objects.all()
    serializer_class = RawParticipantSerializer


class RawContactViewSet(viewsets.ModelViewSet):
    queryset = RawContact.objects.all()
    serializer_class = RawContactSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
