from helpdesk_app.forms import ResourceForm
from helpdesk_app.views import delete_resource
from helpdesk_app.models import AnswerResource
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

class ResourceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='admin', email='admin@admin.com', password='admin'
        )

        self.sample_resource = AnswerResource.objects.create(
            title="Carnegie Mellon",
            url="http://www.cmu.edu",
            blurb="An exmaple resource that points to CMU."
        )

    def test_resource_created(self):
        self.assertIsNotNone(AnswerResource.objects.get(id=1))

    def test_delete_resource(self):
        # Ensure at least one object in the database so far
        self.assertEqual(AnswerResource.objects.all().count(), 1)

        # Prepare request object
        resource_id = self.sample_resource.id
        request = self.factory.get('/update_resource/' + str(resource_id))
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        
        # Same as making a GET request to '/delete_resource/1')
        delete_resource(request, resource_id)

        # Ensure the object has been deleted
        self.assertEqual(AnswerResource.objects.all().count(), 0)

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

    def test_invalid_form4(self):
        form_data = {
            'title' : "Some title here",
            # Duplicate URL with self.sample_resource
            'url' : "http://www.cmu.edu", 
            'blurb' : "Here is a short blurb about the example resource.", 
        }
        form = ResourceForm(data=form_data)
        self.assertFalse(form.is_valid())