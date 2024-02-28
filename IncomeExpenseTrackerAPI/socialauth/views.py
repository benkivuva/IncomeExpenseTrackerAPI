from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer

class GoogleSocialAuthView(GenericAPIView):
    """
    View for authenticating users via Google OAuth.

    Endpoint: /auth/google/

    HTTP Methods:
        - POST: Authenticates the user using the provided authentication token.
    """

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST method to authenticate user via Google OAuth.

        Args:
            request (HttpRequest): The request object containing the authentication token.

        Returns:
            Response: User information or error message along with HTTP status code.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)