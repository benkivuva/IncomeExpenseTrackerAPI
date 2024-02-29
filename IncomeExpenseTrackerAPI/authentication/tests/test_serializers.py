# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.test import TestCase
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import RefreshToken
# from authentication.models import User
# from authentication.serializers import (RegisterSerializer, EmailVerificationSerializer,
#                                         LoginSerializer, ResetPasswordEmailRequestSerializer,
#                                         SetNewPasswordSerializer, LogoutSerializer)

# UserModel = get_user_model()


# class TestRegisterSerializer(TestCase):
#     # def test_validate_username_alphanumeric(self):
#     #     serializer = RegisterSerializer()
#     #     valid_data = {'email': 'test@example.com', 'username': 'test123', 'password': 'testpassword'}
#     #     invalid_data = {'email': 'test@example.com', 'username': 'test@123', 'password': 'testpassword'}

#     #     validated_data = serializer.validate(valid_data)
#     #     self.assertEqual(validated_data, valid_data)

#     #     with self.assertRaises(AuthenticationFailed):
#     #         serializer.validate(invalid_data)


# class TestLoginSerializer(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user = UserModel.objects.create_user(email='test@example.com', username='testuser', password='password')

#     # def test_validate_valid_credentials(self):
#     #     serializer = LoginSerializer()
#     #     valid_data = {'email': 'test@example.com', 'password': 'password'}

#     #     validated_data = serializer.validate(valid_data)
#     #     self.assertEqual(validated_data['email'], valid_data['email'])
#     #     self.assertEqual(validated_data['username'], self.user.username)

#     def test_validate_invalid_credentials(self):
#         serializer = LoginSerializer()
#         invalid_data = {'email': 'test@example.com', 'password': 'wrongpassword'}

#         with self.assertRaises(AuthenticationFailed):
#             serializer.validate(invalid_data)


# class TestSetNewPasswordSerializer(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user = UserModel.objects.create_user(email='test@example.com', username='testuser', password='password')
#         cls.uidb64 = PasswordResetTokenGenerator().make_token(cls.user)
#         cls.token = RefreshToken.for_user(cls.user)

#     # def test_validate_reset_link(self):
#     #     serializer = SetNewPasswordSerializer()
#     #     valid_data = {'password': 'newpassword', 'token': str(self.token), 'uidb64': self.uidb64}

#     #     validated_data = serializer.validate(valid_data)
#     #     self.assertEqual(validated_data, self.user)

#     def test_validate_invalid_reset_link(self):
#         serializer = SetNewPasswordSerializer()
#         invalid_data = {'password': 'newpassword', 'token': 'invalidtoken', 'uidb64': 'invaliduidb64'}

#         with self.assertRaises(AuthenticationFailed):
#             serializer.validate(invalid_data)