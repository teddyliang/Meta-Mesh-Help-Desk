from helpdesk_app.views import autocomplete_search, new_resource
from helpdesk_app.models import AnswerResource, Category
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

class AutocompleteTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Create an admin user to test with
        self.user = User.objects.create_user(
            username='admin', email='admin@admin.com', password='admin'
        )

        self.sample_category1 = Category.objects.create(
            category_name="Category1"
        )
        self.sample_category2 = Category.objects.create(
            category_name="Category2"
        )

        # Create a sample resource by mimicking the HTTP POST call for the form  
        request = self.factory.post(
            '/new_resource/',
            data = {
                'title': 'Carnegie Mellon',
                'url': 'http://www.cmu.edu',
                'blurb': 'An exmaple resource that points to CMU.',
                'tags': 'cmu, test resource, carnegie mellon',
                'categories': [str(self.sample_category1.id)]
            }
        )
        # Submit the request
        request.user = self.user
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        new_resource(request)

        # Create second sample resource
        request = self.factory.post(
            '/new_resource/',
            data = {
                'title': 'How to Properly Restart a Router and Modem',
                'url': 'https://www.lifewire.com/how-to-properly-restart-a-router-modem-2624570',
                'blurb': 'steps to restart a router and modem',
                'tags': 'router, modem, restart',
                'categories': [str(self.sample_category2.id)]

            }
        )
        # Submit the second request
        request.user = self.user
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        new_resource(request)

    def test_resource_created(self):
        # Ensures the setup was successful
        self.assertEquals(AnswerResource.objects.all().count(), 2)
        self.assertEquals(len(list(AnswerResource.objects.first().tags.names())), 3)

    def test_autocomplete_existing_result(self):
        # Prepare request object
        request = self.factory.get('/autocomplete?term=cmu')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Same as making a GET request to '/autocomplete')
        response = autocomplete_search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))

        # Ensure a response was returned
        self.assertEquals(decoded_response.find("No results found"), -1)
        # Ensure the right resource was returned by the model
        self.assertNotEqual(decoded_response.find("Carnegie Mellon"), -1)

    def test_autocomplete_existing_result_with_query_stopwords(self):
        # Prepare request object
        request = self.factory.get('/autocomplete?term=how%20to')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Same as making a GET request to '/autocomplete')
        response = autocomplete_search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        # Ensure a response was returned
        self.assertEquals(decoded_response.find("No results found"), -1)
        # Ensure the right resource was returned by the model
        self.assertNotEqual(decoded_response.find("How to Properly Restart a Router"), -1)

    def test_autocomplete_no_result(self):
        # Prepare request object
        request = self.factory.get('/autocomplete?term=random')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Same as making a GET request to '/autocomplete')
        response = autocomplete_search(request)
        decoded_response = ''.join(filter(str.isalnum, str(response.content.decode('utf-8').rstrip().split('\n'))))

        # Ensure a response was NOT returned
        self.assertEqual(decoded_response, "")

    def test_autocomplete_different_category_no_result(self):
        # Prepare request object
        request = self.factory.get('/autocomplete?term=restart&c=Category1')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Same as making a GET request to '/autocomplete')
        response = autocomplete_search(request)
        decoded_response = ''.join(filter(str.isalnum, str(response.content.decode('utf-8').rstrip().split('\n'))))

        # Ensure a response was NOT returned
        self.assertEqual(decoded_response, "")