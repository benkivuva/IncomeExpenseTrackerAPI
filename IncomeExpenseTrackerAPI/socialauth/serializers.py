from rest_framework import serializers
from . import google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class GoogleSocialAuthSerializer(serializers.Serializer):
    """
    Serializer for validating Google social authentication token.
    """

    auth_token = serializers.CharField(help_text="Google authentication token.")

    def validate_auth_token(self, auth_token):
        """
        Validate the provided Google authentication token.

        Args:
            auth_token (str): The Google authentication token to validate.

        Returns:
            dict: User data retrieved from Google.

        Raises:
            serializers.ValidationError: If the token is invalid or expired.
            AuthenticationFailed: If the token does not match the expected audience.

        """
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.getenv('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)