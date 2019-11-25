# -*- coding: utf-8 -*-

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
from django.contrib.auth.models import User
from oauth2_provider.models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from templates import *
from weasyprint import HTML
import tempfile
from django.template.loader import render_to_string
from itertools import groupby


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


class MissingTokenException(APIException):
    status_code = 401
    default_detail = 'Token expirado'
    default_code = 'expired_token'


class UserInfoToken(APIView):
    def get(self, request, token):
        try:
            userToken = AccessToken.objects.get(token=token)
            if str(userToken.expires) > str(datetime.now()):
                user = User.objects.get(id=userToken.user.id)
                group = Group.objects.filter(user=userToken.user.id).count()
                obj = {'id': user.id, 
                    'username': user.username,
                    'is_active': user.is_active, 
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff, 
                    'group_count': group}
                return Response(obj)
            else:
                raise MissingTokenException
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("ObjectDoesNotExist para el token" + token)


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


def PDFGeneral(request):

        #Modelos
        escuelas = RawSchool.objects.all()
        concurso = Contest.objects.filter(is_active=True)
        cantidad_grupos = Group.objects.count()
        proyecto = RawProject.objects.all()
        
        
        datos = {
            'tipo_escuela': escuelas,
            'datos_concurso': concurso,
            'cantidad_grupos': cantidad_grupos,
            'nombre_proyecto': proyecto,
            'difusion': proyecto,
            'diffusion_count': {}
        }
                
        tipo = []
        for proyectos in proyecto:
            tipo.append(proyectos.get_diffusion_display())
            
        for k in RawProject.DIFFUSION:
            datos['diffusion_count'][k[1]] = 0

        for i in tipo:
            datos['diffusion_count'][i] = tipo.count(i)        
        print(datos)

        #Response
        rendered_html = render_to_string('export_contest.html', datos)
        response = HttpResponse(content_type='application/pdf')
        pdf = HTML(string=rendered_html).write_pdf(response, presentational_hints=True)
        return response
    
def PDFEspecifico(request, id):

        #Modelos
        contact = RawContact.objects.get(group=id)
        escuelas = RawSchool.objects.get(group=id)
        proyecto = RawProject.objects.get(group=id)
        participant = RawParticipant.objects.filter(group=id)

        print(participant)
        datos = {
            'contact': contact,
            'school': escuelas,
            'project': proyecto,
            'participant': participant,
            'category': proyecto.category.all().values('name')
            
        }

        #Response
        rendered_html = render_to_string('export_group.html', datos)
        response = HttpResponse(content_type='application/pdf')
        pdf = HTML(string=rendered_html).write_pdf(response, presentational_hints=True)
        return response