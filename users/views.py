import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import SignUpSerializer, UserSerializer
from .models import User


class SignUpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed('There is no such user!')

        if email is None:
            raise AuthenticationFailed('Please enter the email!')

        if password is None:
            raise AuthenticationFailed('Please enter the password!')

        access_token = user.token
        refresh_token = user.refresh_token

        response = Response()

        response.set_cookie(key='access', value=access_token, httponly=True)
        response.set_cookie(key='refresh', value=refresh_token, httponly=True)

        response.data = {
            'access': access_token,
            'refresh': refresh_token
        }

        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('access')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            user = User.objects.filter(id=payload['id']).first()
        except User.DoesNotExist:
            raise AuthenticationFailed('Unauthenticated')

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.data = {
            'message': 'success'
        }
        return response


class RefreshTokenView(APIView):

    def post(self, request):

        refresh_token = request.COOKIES.get('refresh')

        if not refresh_token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            user = User.objects.filter(id=payload['id']).first()
        except User.DoesNotExist:
            raise AuthenticationFailed('Unauthenticated')

        response = Response()
        response.data = {
            'access': user.token,
            'refresh': user.refresh_token
        }

        return response
