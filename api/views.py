import time
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Profile, Token
from .serializers import SignupSerializer, SigninSerializer, InfoSerializer, LogoutSerializer

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['id']
            password = serializer.validated_data['password']

            # Определяем тип id: email если содержит @, иначе phone
            if '@' in user_id:
                id_type = 'email'
            else:
                id_type = 'phone'

            # Проверяем, существует ли уже пользователь с таким username
            if User.objects.filter(username=user_id).exists():
                return Response({'error': 'Пользователь с таким ID уже существует.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Создаём пользователя
            user = User.objects.create_user(username=user_id, password=password)
            # Создаём профиль с типом id
            Profile.objects.create(user=user, id_type=id_type)

            # Генерируем токен
            token = Token.generate_token(user)

            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['id']
            password = serializer.validated_data['password']

            user = authenticate(username=user_id, password=password)
            if user is None:
                return Response({'error': 'Неверные учетные данные.'}, status=status.HTTP_400_BAD_REQUEST)

            # Генерируем новый токен
            token = Token.generate_token(user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoView(APIView):
    def get(self, request):
        # request.user гарантированно установлен нашим authentication-классом
        serializer = InfoSerializer(request.user)
        return Response(serializer.data)


class LatencyView(APIView):
    def get(self, request):
        try:
            start = time.time()
            response = requests.get('https://ya.ru', timeout=5)
            end = time.time()
            latency_ms = int((end - start) * 1000)
            return Response({'latency_ms': latency_ms})
        except requests.RequestException:
            return Response({'error': 'Не удалось получить ответ от ya.ru'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            delete_all = serializer.validated_data['all']
            token = request.auth  # наш кастомный authentication возвращает токен во втором элементе

            if delete_all:
                # Удаляем все токены пользователя
                Token.objects.filter(user=request.user).delete()
            else:
                # Удаляем только текущий токен
                if token:
                    token.delete()
            return Response({'detail': 'Вы успешно вышли.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
