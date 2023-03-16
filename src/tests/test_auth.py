from django.contrib.auth.models import User
from helpdesk_app.forms import SignUpForm
from django.test import TestCase

class RegistrationTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'username' : "example_username",
            'email' : "example@example.com", 
            'password1' : "p@ssword123", 
            'password2' : "p@ssword123",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username' : "example_username",
            'email' : "example@example.com", 
            # Password used is too common
            'password1' : "password123", 
            'password2' : "password123",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form2(self):
        form_data = {
            'username' : "example_username",
            'email' : "example@example.com",
            'password1' : "password123",
            # Invalid confirmation
            'password2' : "password12345",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form3(self):
        form_data = {
            'username' : "example_username",
            # Missing required data (email)
            'password1' : "p@ssword123",
            'password2' : "p@ssword123",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

class LogInTest(TestCase):
    def setUp(self):
        self.creds = {
            'username': 'example_username',
            'password': 'password123'
        }
        User.objects.create_user(**self.creds)

    def test_login(self):
        response = self.client.post('/login/', self.creds, follow=True)
        self.assertTrue(response.context['user'].is_active)