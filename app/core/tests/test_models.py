from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='test@fok.com', password= 'testpass'):
    """ Create a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with email """

        email = 'ifokito@johnthegreek.gr'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
    
    def test_user_email_is_normalized(self):
        """ Test that the second part of the email is all lower case """

        email = 'fok@THEGREEK.COM'
        user = get_user_model().objects.create_user(email,'test123')
        
        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """ Test that the user is not allowed to register without an email """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    
    def test_create_new_superuser(self):
        """ Test creating a new super user """

        user = get_user_model().objects.create_superuser(
            'test@thegreek.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
        