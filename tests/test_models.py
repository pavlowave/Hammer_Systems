from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_invite_code_generation(self):
        user = User.objects.create(phone_number='+1234567890')
        self.assertEqual(len(user.invite_code), 6)
        self.assertTrue(user.invite_code.isalnum())

    def test_invited_by_relationship(self):
        inviter = User.objects.create(phone_number='+1111111111')
        invitee = User.objects.create(phone_number='+2222222222', invited_by=inviter)
        self.assertEqual(invitee.invited_by, inviter)
        self.assertIn(invitee, inviter.invited_users.all())

    def test_invite_code_uniqueness(self):
        user1 = User.objects.create(phone_number='+1234567890')
        user2 = User.objects.create(phone_number='+9876543210')
        self.assertNotEqual(user1.invite_code, user2.invite_code)
