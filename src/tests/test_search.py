from helpdesk_app.views import search, new_resource
from helpdesk_app.models import AnswerResource, Category
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

class SearchTests(TestCase):
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
        self.assertEquals(decoded_response.find("No results found"), -1)
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
        self.assertNotEqual(decoded_response.find("No results found"), -1)

    def test_search_category_valid(self):
        # Prepare request object
        # This time, we are setting the category parameter to category 1, which our sample resource belongs to
        request = self.factory.get('/search?q=cmu&c=' + self.sample_category1.category_name)
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        
        # Same as making a GET request to '/search')
        response = search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        
        # Ensure a response was returned
        self.assertEquals(decoded_response.find("No results found"), -1)
        # Ensure the right resource was returned by the model
        self.assertNotEqual(decoded_response.find("http://www.cmu.edu"), -1)
    
    def test_search_category_no_result(self):
        # Prepare request object
        # This time, we are setting the category parameter to category 2, which
        # our sample resource DOES NOT belong to
        request = self.factory.get('/search?q=cmu&c=' + self.sample_category2.category_name)
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        
        # Same as making a GET request to '/search')
        response = search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        
        # Ensure a response was NOT returned
        self.assertNotEqual(decoded_response.find("No results found"), -1)

    def test_search_special_characters_no_results(self):
        # Prepare request object
        request = self.factory.get('/search?q=\" ^ \' - +  ^^ \'\' -- ++')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        
        # Same as making a GET request to '/search')
        response = search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        
        # Ensure a response was NOT returned
        self.assertNotEqual(decoded_response.find("No results found"), -1)