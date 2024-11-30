from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField(help_text='Список номеров телефонов пользователей, приглашённых данным пользователем.')

    phone_number = serializers.CharField(
        help_text='Номер телефона пользователя в формате +7XXXXXXXXXX'
    )
    invite_code = serializers.CharField(
        help_text='Уникальный инвайт-код пользователя, если он существует.',
        required=False
    )
    invited_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text='ID пользователя, который пригласил данного пользователя. Может быть пустым.',
        allow_null=True,
        required=False
    )

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'invited_by', 'invited_users']

    def get_invited_users(self, obj):
        '''
        Возвращает список номеров телефонов пользователей,
        которые были приглашены данным пользователем.
        '''
        return [user.phone_number for user in obj.invited_users.all()]
