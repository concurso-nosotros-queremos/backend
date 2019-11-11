from rest_framework import viewsets
from .serializers import *
from .serializers import MessageEmailSerializer
from cnq.models import *
from .permissions import MyUserPermissions, ContestPermissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from guardian.shortcuts import get_objects_for_user
from rest_framework import generics
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


class ContestEnd(viewsets.ViewSet):
    permission_classes = (IsAdminUser, )
    def list(self, request):
        queryset = Contest.objects.filter(is_active=True)
        serializer = ContestSerializerEnd(queryset, many=True)
        return Response(serializer.data)

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (MyUserPermissions, IsAuthenticated, ContestPermissions)
    def get_queryset(self):
        groups = get_objects_for_user(self.request.user, 'cnq.view_group')
        return groups


class GroupCount(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsAdminUser )

    def get(self, request, format=None):
        groups = Group.objects.count()
        content = {'total': groups}
        return Response(content)

        
class GroupCity(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city', None)
        queryset = Group.objects.all()
        if city is not None:
            raw_school_queryset = RawSchool.objects.filter(city__id=city)
            ids = [s.group.id for s in raw_school_queryset]
            queryset = queryset.filter(id__in=ids)
        return queryset


class GroupState(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        state = self.request.query_params.get('state', None)
        queryset = Group.objects.all()
        if state is not None:
            raw_school_queryset = RawSchool.objects.filter(city__state=state)
            ids = [s.group.id for s in raw_school_queryset]
            queryset = queryset.filter(id__in=ids)
        return queryset
        
        
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
    permission_classes = (IsAuthenticated, )

class CheckToken(generics.CreateAPIView):
    serializer_class = TokenSerializer
    permission_classes = (IsAuthenticated, )


class TokenUsesViewSet(viewsets.ModelViewSet):
    queryset = TokenUses.objects.all()
    serializer_class = TokenUsesSerializer


class RawParticipantViewSet(viewsets.ModelViewSet):
    queryset = RawParticipant.objects.all()
    serializer_class = RawParticipantSerializer

class RawParticipantCount(generics.ListAPIView):
    serializer_class = RawParticipantSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, format=None):
        participants = RawParticipant.objects.count()
        content = {'total': participants}
        return Response(content)


class RawContactViewSet(viewsets.ModelViewSet):
    queryset = RawContact.objects.all()
    serializer_class = RawContactSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer


class MessageEmailViewSet(viewsets.ModelViewSet):
    queryset = MessageEmail.objects.all()
    serializer_class = MessageEmailSerializer