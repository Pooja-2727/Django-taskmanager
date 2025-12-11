# tasks/management/commands/create_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tasks.models import Task

class Command(BaseCommand):
    help = "Create Admin and User groups for RBAC."

    def handle(self, *args, **options):
        admin_group, created = Group.objects.get_or_create(name="Admin")
        user_group, created2 = Group.objects.get_or_create(name="User")

        # Give Admin full permissions on Task model
        content_type = ContentType.objects.get_for_model(Task)
        perms = Permission.objects.filter(content_type=content_type)
        admin_group.permissions.set(perms)

        # For 'User' group we do NOT assign model-level permissions: we enforce owner-only
        self.stdout.write(self.style.SUCCESS("Groups 'Admin' and 'User' ensured."))
