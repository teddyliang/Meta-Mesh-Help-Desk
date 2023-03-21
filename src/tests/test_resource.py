from django.contrib.auth.models import User
from helpdesk_app.forms import SignUpForm, ResourceForm
from django.test import TestCase

class ResourceTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'title' : "Example Resource",
            'url' : "http://www.google.com", 
            'blurb' : "Here is a short blurb about the example resource.", 
        }
        form = ResourceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'title' : "Example Resource",
            # Invalid URL
            'url' : "this is not a valid url", 
            'blurb' : "Here is a short blurb about the example resource.", 
        }
        form = ResourceForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form2(self):
        form_data = {
            # Title too long
            'title' : "Instead of a short title, I'm instead writing a very long description instead which should throw an error!",
            'url' : "http://www.google.com", 
            'blurb' : "Here is a short blurb about the example resource.", 
        }
        form = ResourceForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form3(self):
        form_data = {
            # Missing parameters
            'title' : "",
            'url' : "http://www.google.com", 
            'blurb' : "Here is a short blurb about the example resource.", 
        }
        form = ResourceForm(data=form_data)
        self.assertFalse(form.is_valid())