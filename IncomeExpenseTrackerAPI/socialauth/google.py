from google.auth.transport import requests
from google.oauth2 import id_token

class Google:
    """Utility class for Google OAuth operations."""

    @staticmethod
    def validate(auth_token):
        """
        Validate method queries the Google OAuth2 API to fetch user information.

        Args:
            auth_token (str): The authentication token provided by Google.

        Returns:
            dict or str: User information if the token is valid, otherwise an error message.
        """
        try:
            # Verify the OAuth2 token
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            # Check if the token is issued by Google
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except Exception as e:
            # Handle token validation errors
            return "The token is either invalid or has expired"