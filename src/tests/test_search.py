from helpdesk_app.views import search, new_resource
from helpdesk_app.models import AnswerResource
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

class ResourceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Create an admin user to test with
        self.user = User.objects.create_user(
            username='admin', email='admin@admin.com', password='admin'
        )

        # Create a sample resource by mimicking the HTTP POST call for the form  
        request = self.factory.post(
            '/new_resource/',
            data = {
                'title': 'Carnegie Mellon',
                'url': 'http://www.cmu.edu',
                'blurb': 'An exmaple resource that points to CMU.',
                'tags': 'cmu, test resource, carnegie mellon'
            }
        )
        # Submit the request
        request.user = self.user
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        new_resource(request)

    def test_resource_created(self):
        # Ensures the setup was successful
        self.assertEquals(AnswerResource.objects.all().count(), 1)
        self.assertEquals(len(list(AnswerResource.objects.first().tags.names())), 3)

    def test_search_valid_result(self):
        # Prepare request object
        request = self.factory.get('/search?q=cmu')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        
        # Same as making a GET request to '/search')
        response = search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        
        # Ensure a response was returned
        self.assertEquals(decoded_response.find("No matches found"), -1)
        # Ensure the right resource was returned by the model
        self.assertNotEqual(decoded_response.find("http://www.cmu.edu"), -1)

    def test_search_no_result(self):
        # Prepare request object
        request = self.factory.get('/search?q=random')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        
        # Same as making a GET request to '/search')
        response = search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        
        # Ensure a response was NOT returned
        self.assertNotEqual(decoded_response.find("No matches found"), -1)