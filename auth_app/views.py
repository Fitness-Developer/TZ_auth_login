from django.urls import path
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer,UpdateUserSerializer
from .models import User, AuthToken, Role, UserRole
from .utils import generate_salt, hash_password, generate_token, token_expiry
from datetime import datetime



@api_view(['POST'])
def register(request):
    s = RegisterSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=400)
    data = s.validated_data
    salt = generate_salt()
    hashed = hash_password(salt, data['password'])
    user = User.objects.create(
        first_name=data['first_name'],
        last_name=data.get('last_name', ''),
        middle_name=data.get('middle_name', ''),
        email=data['email'],
        password_hash=hashed,
        salt=salt,
        is_active=True
    )
    role, _ = Role.objects.get_or_create(name='user')
    UserRole.objects.create(user=user, role=role)
    return Response({'id': str(user.id)}, status=201)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'detail': 'email and password required'}, status=400)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail': 'invalid credentials'}, status=401)
    hashed = hash_password(user.salt, password)
    if hashed != user.password_hash or not user.is_active:
        return Response({'detail': 'invalid credentials or inactive'},status=401)
    token_value = generate_token()
    expires = token_expiry()
    token = AuthToken.objects.create(user=user, token=token_value, expires_at=expires)
    return Response({'token': token.token, 'expires_at': expires.isoformat()})

@api_view(['POST'])
def logout(request):
    token_obj = getattr(request, '_auth_token', None)
    if token_obj:
        token_obj.delete()
        return Response({'detail': 'logged out'})
    return Response({'detail': 'Unauthorized'}, status=401)

@api_view(['GET','PUT','DELETE'])
def user_profile(request):
    auth_header = request.headers.get('Authorization')
    print("Authorization header:", auth_header)  # <- проверка
    if not auth_header:
        return Response({'detail': 'Unauthorized'}, status=401)
    try:
        prefix, token_value = auth_header.split()
        print("Prefix:", prefix, "Token:", token_value)  # <- проверка
        if prefix != 'Token':
            return Response({'detail': 'Unauthorized'}, status=401)
        token = AuthToken.objects.filter(token=token_value, expires_at__gt=datetime.utcnow()).first()
        if not token:
            return Response({'detail': 'Unauthorized'}, status=401)
        user = token.user
        if not user.is_active:
            return Response({'detail': 'Unauthorized'}, status=401)
    except Exception as e:
        print("Exception:", e)
        return Response({'detail': 'Unauthorized'}, status=401)

    if request.method == 'GET':
        return Response(UserSerializer(user).data)

    if request.method == 'PUT':
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        for k, v in serializer.validated_data.items():
            setattr(user, k, v)
        user.save()
        return Response(UserSerializer(user).data)

    if request.method == 'DELETE':
        user.is_active = False
        user.save()
        AuthToken.objects.filter(user=user).delete()
        return Response({'detail': 'account deactivated'})

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('user/', user_profile),
]
