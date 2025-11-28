from rest_framework import serializers
from .models import Resource, Permission

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'code', 'description')

class PermissionSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(read_only=True)
    resource_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Permission
        fields = ('id', 'resource', 'resource_id', 'action')