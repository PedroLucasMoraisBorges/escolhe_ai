from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=244, default='', unique=True)
    email = models.EmailField(unique = True, blank = True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        blank=True
    )

    def __str__(self):
        return self.username