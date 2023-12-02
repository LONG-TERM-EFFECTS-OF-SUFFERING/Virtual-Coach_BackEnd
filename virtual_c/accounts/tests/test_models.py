from django.test import TestCase
from accounts.models import UserAccount

class TestUserAccountModel(TestCase):
    def setUp(self):
        self.test_user = UserAccount.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )

    def test_user_account_creation(self):
        self.assertEqual(self.test_user.email, 'testuser@example.com')
        self.assertEqual(self.test_user.name, 'Test User')
        self.assertTrue(self.test_user.is_active)
        self.assertFalse(self.test_user.is_staff)
        self.assertFalse(self.test_user.is_superuser)

    def test_user_account_modification(self):
        self.test_user.email = 'modifieduser@example.com'
        self.test_user.name = 'Modified User'
        self.test_user.save()

        modified_user = UserAccount.objects.get(email='modifieduser@example.com')

        self.assertEqual(modified_user.email, 'modifieduser@example.com')
        self.assertEqual(modified_user.name, 'Modified User')

    def test_user_account_read(self):
        retrieved_user = UserAccount.objects.get(id=self.test_user.id)

        self.assertEqual(retrieved_user.email, 'testuser@example.com')
        self.assertEqual(retrieved_user.name, 'Test User')

    def test_user_account_deletion(self):
        self.test_user.delete()

        with self.assertRaises(UserAccount.DoesNotExist):
            deleted_user = UserAccount.objects.get(id=self.test_user.id)

