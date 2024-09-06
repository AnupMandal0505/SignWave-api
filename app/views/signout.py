from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  # Import RefreshToken for JWT blacklisting

class LogoutAPI(APIView):
    def post(self, request):
        # Assuming you're using JWT and the token is included in the request headers
        token = request.headers.get('Authorization').split()[1]

        try:
            # Blacklist the token
            # Note: This is a conceptual example. You need to implement your own logic for blacklisting tokens.
            # This might involve using a cache like Redis or in-memory storage.
            # For now, we're just showing how to blacklist using the token's jti (JWT ID).
            # Make sure to handle token expiration if needed.
            decoded_token = RefreshToken(token)
            decoded_token.blacklist()

            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
