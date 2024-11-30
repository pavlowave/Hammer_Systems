import random
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from .serializers import UserSerializer

User = get_user_model()


class PhoneAuthView(APIView):
    codes = {}

    @swagger_auto_schema(
        operation_summary='Отправить код подтверждения',
        operation_description='Генерирует код подтверждения и отправляет его по указанному номеру телефона.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер телефона')
            },
            required=['phone_number']
        ),
        responses={
            200: openapi.Response(
                description='Код отправлен',
                examples={'application/json': {'message': 'Code sent', 'code': 1234}}
            ),
            400: openapi.Response(description='Ошибка: номер телефона не указан')
        }
    )
    def post(self, request, format=None):
        phone_number = request.data.get('phone_number')
        if phone_number:
            code = random.randint(1000, 9999)
            self.codes[phone_number] = code
            time.sleep(1)
            return Response({'message': 'Code sent', 'code': code})
        return Response({'error': 'Phone number required'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Проверить код подтверждения',
        operation_description='Проверяет код подтверждения и аутентифицирует пользователя. Если пользователь новый, создаёт его.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер телефона'),
                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='Код подтверждения')
            },
            required=['phone_number', 'code']
        ),
        responses={
            200: openapi.Response(
                description='Успешная аутентификация',
                schema=UserSerializer
            ),
            400: openapi.Response(description='Ошибка: код некорректный или не указан')
        }
    )
    def put(self, request, format=None):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        if self.codes.get(phone_number) == int(code):
            user, created = User.objects.get_or_create(phone_number=phone_number)
            return Response({'message': 'Authenticated', 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    @swagger_auto_schema(
        operation_summary='Получить профиль пользователя',
        operation_description='Возвращает профиль пользователя на основе номера телефона.',
        manual_parameters=[
            openapi.Parameter(
                'phone_number',
                openapi.IN_QUERY,
                description='Номер телефона пользователя',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='Профиль пользователя',
                schema=UserSerializer
            ),
            404: openapi.Response(description='Пользователь не найден')
        }
    )
    def get(self, request, format=None):
        phone_number = request.query_params.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            return Response(UserSerializer(user).data)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Активировать инвайт-код',
        operation_description='Привязывает пользователя к пригласившему по указанному инвайт-коду.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер телефона пользователя'),
                'invite_code': openapi.Schema(type=openapi.TYPE_STRING, description='Инвайт-код пригласившего')
            },
            required=['phone_number', 'invite_code']
        ),
        responses={
            200: openapi.Response(
                description='Успешная активация инвайт-кода',
                schema=UserSerializer
            ),
            400: openapi.Response(description='Ошибка: некорректные данные или код уже активирован')
        }
    )
    def post(self, request, format=None):
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')
        user = User.objects.filter(phone_number=phone_number).first()
        inviter = User.objects.filter(invite_code=invite_code).first()
        if user and inviter:
            if user.invited_by:
                return Response({'error': 'Invite code already activated'}, status=status.HTTP_400_BAD_REQUEST)
            user.invited_by = inviter
            user.save()
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


def phone_auth_html(request):
    '''Рендеринг HTML для авторизации по номеру телефона и просмотра профиля.'''
    return render(request, 'phone_auth_html.html')