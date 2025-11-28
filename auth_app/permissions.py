from rest_framework.permissions import BasePermission
from access_control.models import Permission as AC_Permission, Resource,RolePermission, Role


class HasResourcePermission(BasePermission):
    action_map = {
        'GET': 'read',
        'POST': 'create',
        'PUT': 'update',
        'PATCH': 'update',
        'DELETE': 'delete'
    }

    def has_permission(self, request, view):
        if not getattr(request, 'user', None):
            return False
        resource_code = getattr(view, 'resource_code', None)
        if not resource_code:
            return True
        action = self.action_map.get(request.method, None)
        if not action:
            return False
        try:
            resource = Resource.objects.get(code=resource_code)
        except Resource.DoesNotExist:
            return False
        # collect user's roles
        roles = [ur.role for ur in request.user.user_roles.select_related('role')]
        # check role_permissions
        for role in roles:
            if RolePermission.objects.filter(role=role,permission__resource=resource, permission__action=action).exists():
                return True
        return False
