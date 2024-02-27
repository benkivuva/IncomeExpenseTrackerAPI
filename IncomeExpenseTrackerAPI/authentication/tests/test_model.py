from .test_setup import TestSetUp
from ..models import User


class TestUserModel(TestSetUp):

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_verified)
        self.assertTrue(user.is_active)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertEqual(user.auth_provider, 'email')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.user_data)
        self.assertEqual(superuser.username, self.user_data['username'])
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertFalse(superuser.is_verified)
        self.assertTrue(superuser.is_active)
        self.assertIsNotNone(superuser.created_at)
        self.assertIsNotNone(superuser.updated_at)
        self.assertEqual(superuser.auth_provider, 'email')