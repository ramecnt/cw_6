from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from mailing.models import Mailing, Client, Blog


class Command(BaseCommand):
    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name='manager')
        permissions = [
            f'add_blog',
            f'delete_client',
            f'delete_mailing',
        ]
        for permission in permissions:
            permission_obj = Permission.objects.get(
                codename=permission
            )
            manager_group.permissions.add(permission_obj)
