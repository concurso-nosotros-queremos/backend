from rest_framework import permissions

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
