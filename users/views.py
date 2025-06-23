from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import ConfirmationCode
from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(username=username, password=password, is_active=False)

        code = ConfirmationCode.generate_code()
        ConfirmationCode.objects.create(user=user, code=code)

        return Response({'message': 'User created. Use confirmation code.', 'code': code},
                        status=status.HTTP_201_CREATED)


class ConfirmationAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(username=username)
            confirm = ConfirmationCode.objects.get(user=user)
        except (User.DoesNotExist, ConfirmationCode.DoesNotExist):
            return Response({'error': 'Invalid user or code'},
                            status=status.HTTP_400_BAD_REQUEST)

        if confirm.code != code:
            return Response({'error': 'Incorrect code'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        confirm.delete()

        return Response({'message': 'Account confirmed. You can now log in.'}, status=status.HTTP_200_OK)


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user:
            if not user.is_active:
                return Response({'error': 'Account is not active'}, status=status.HTTP_403_FORBIDDEN)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response(status=status.HTTP_401_UNAUTHORIZED)
