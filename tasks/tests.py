# tasks/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Task

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.task = Task.objects.create(owner=self.user, title='T1')

    def test_task_created(self):
        self.assertEqual(self.task.owner, self.user)
        self.assertFalse(self.task.status)

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user1', password='pass1')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        # create roles
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='User')

    def test_register_and_login(self):
        resp = self.client.post('/api/auth/register/', {'username':'newu', 'password':'newpass'})
        self.assertEqual(resp.status_code, 201)
        login = self.client.post('/api/auth/login/', {'username':'newu', 'password':'newpass'})
        self.assertEqual(login.status_code, 200)
        self.assertIn('access', login.data)
