from django.db import models
import uuid
from auth_app.models import Role


class Resource(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code

class Permission(models.Model):
    ACTIONS = [
        ('read', 'read'),
        ('create', 'create'),
        ('update', 'update'),
        ('delete', 'delete'),
    ]
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE,related_name='permissions')
    action = models.CharField(max_length=20, choices=ACTIONS)

    class Meta:
        unique_together = ('resource', 'action')

    def __str__(self):
        return f"{self.resource.code}:{self.action}"

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_roles')

    class Meta:
        unique_together = ('role', 'permission')