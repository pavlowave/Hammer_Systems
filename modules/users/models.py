import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

def generate_invite_code():
    '''
    Генерирует уникальный инвайт-код длиной 6 символов,
    состоящий из букв и цифр.
    '''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


class UserManager(BaseUserManager):
    '''
    Менеджер для создания пользователей.
    Метод create_user используется для создания пользователя по номеру телефона.
    '''
    def create_user(self, phone_number):
        '''
        Создаёт и сохраняет пользователя с указанным номером телефона.
        '''
        user = self.model(phone_number=phone_number)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    Модель пользователя, которая включает:
    - телефонный номер
    - уникальный инвайт-код
    - пользователя, который пригласил этого пользователя
    '''

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text='Номер телефона пользователя в формате +7XXXXXXXXXX. Должен быть уникальным.'
    )
    invite_code = models.CharField(
        max_length=6,
        unique=True,
        default=generate_invite_code,
        help_text='Уникальный инвайт-код, генерируется автоматически.'
    )
    invited_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='invited_users',
        help_text='Пользователь, который пригласил данного пользователя. Может быть пустым.'
    )

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        '''
        Возвращает строковое представление пользователя - номер телефона.
        '''
        return self.phone_number
