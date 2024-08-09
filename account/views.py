from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserAccount
from .serializers import UserAccountSerializer
from django.contrib.auth import authenticate


class RegisterView(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserAccountSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = response.data
        return Response({
            'user': user,
            'message': 'User registered successfully.'
        })


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            example={
                'email': 'user@example.com',
                'password': 'stringpassword'
            }
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "access": "your.jwt.access.token"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "error": "Invalid Credentials"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)
