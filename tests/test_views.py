from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(phone_number='+1234567890')
        self.user2 = User.objects.create(phone_number='+9876543210')

    def test_phone_auth(self):
        response = self.client.post('/api/auth/', {'phone_number': '+1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code', response.data)

    def test_activate_invite_code(self):
        response = self.client.post(
            '/api/profile/',
            {'phone_number': '+9876543210', 'invite_code': self.user1.invite_code}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.invited_by, self.user1)

    def test_invited_users_list(self):
        self.user2.invited_by = self.user1
        self.user2.save()

        response = self.client.get('/api/profile/', {'phone_number': '+1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('+9876543210', response.data['invited_users'])
