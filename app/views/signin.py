from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers.LoginSerializer import LoginSerializer
from app.serializers.userSerializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']
                # print("After validation print")

                user = authenticate(username=username, password=password)
                # print("USER DATA",user)
                if user is None:
                    error_response = {
                        'status': 400,
                        'error': 'invalid_password',
                        'message': 'Invalid password',
                        'data': {}
                    }
                    return Response(error_response, status=400)

                refresh = RefreshToken.for_user(user)
                # print("After Refress")
                success_response = {
                    'user': UserSerializer(user, many=False).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(success_response)

            else:
                error_response = {
                    'status': 400,
                    'error': 'invalid_data',
                    'message': 'Invalid data check serializer',
                    'data': {}
                }
                return Response(error_response, status=400)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Not get data',
                'data': {}
            }
            return Response(error_response, status=400)