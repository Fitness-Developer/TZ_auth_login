from django.urls import path
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .models import Resource, Permission, RolePermission
from .serializers import ResourceSerializer, PermissionSerializer
from auth_app.models import Role, UserRole
from django.contrib.auth.models import AnonymousUser
from .authentication import CustomTokenAuthentication

def is_admin(user):
    if not user or isinstance(user, AnonymousUser):
        return False
    return user.user_roles.filter(role__name='admin').exists()


@api_view(['GET', 'POST'])
def roles_view(request):
    if not is_admin(request.user):
        return Response({'detail': 'Forbidden'}, status=403)
    if request.method == 'GET':
        roles = Role.objects.all().values('id', 'name')
        return Response(list(roles))
    if request.method == 'POST':
        name = request.data.get('name')
        if not name:
            return Response({'detail': 'name required'}, status=400)
        role, _ = Role.objects.get_or_create(name=name)
        return Response({'id': role.id, 'name': role.name}, status=201)


@api_view(['GET', 'POST'])
def resources_view(request):
    if not is_admin(request.user):
        return Response({'detail': 'Forbidden'}, status=403)
    if request.method == 'GET':
        qs = Resource.objects.all()
        return Response(ResourceSerializer(qs, many=True).data)
    if request.method == 'POST':
        s = ResourceSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=400)
        res = s.save()
        for action in ['read', 'create', 'update', 'delete']:
            Permission.objects.get_or_create(resource=res, action=action)
        return Response(ResourceSerializer(res).data, status=201)


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
def assign_permission(request):
    if not is_admin(request.user):
        return Response({'detail': 'Forbidden'}, status=403)
    role_id = request.data.get('role_id')
    permission_id = request.data.get('permission_id')
    if not role_id or not permission_id:
        return Response({'detail': 'role_id and permission_id required'}, status=400)
    try:
        role = Role.objects.get(id=int(role_id))
        perm = Permission.objects.get(id=int(permission_id))
    except Exception:
        return Response({'detail': 'role or permission not found'}, status=404)
    RolePermission.objects.get_or_create(role=role, permission=perm)
    return Response({'detail': 'assigned'})


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
def assign_role(request):
    if not is_admin(request.user):
        return Response({'detail': 'Forbidden'}, status=403)
    user_id = request.data.get('user_id')
    role_id = request.data.get('role_id')
    if not user_id or not role_id:
        return Response({'detail': 'user_id and role_id required'}, status=400)
    from auth_app.models import User
    try:
        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
    except Exception:
        return Response({'detail': 'user or role not found'}, status=404)
    UserRole.objects.get_or_create(user=user, role=role)
    return Response({'detail': 'role assigned'})


urlpatterns = [
    path('roles/', roles_view),
    path('resources/', resources_view),
    path('assign-permission/', assign_permission),
    path('assign-role/', assign_role),
]