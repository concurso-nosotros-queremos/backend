from rest_framework import permissions
from cnq.models import *
import datetime
from django.db import Error

class MyUserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser == True:
            return True
        elif view.action == 'destroy':
            return False
        elif user == obj.user:
            return True
        return user.has_perm('view_group', obj)

class ContestPermissions(permissions.BasePermission):
    message = 'Las inscripciones han finalizado'
    def has_permission(self, request, view):
        contest = Contest.objects.get(is_active=True)
        now = datetime.datetime.now().isoformat()
        end = contest.inscription_date_to.isoformat()
        if view.action == 'create' and now > end:
            return False
        return True