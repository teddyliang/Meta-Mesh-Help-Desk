from helpdesk_app.views import thumbs_down_clicked, new_resource, resource_appeared, resource_clicked
from helpdesk_app.models import AnswerResource, Category
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

class ResourceStatsTests(TestCase):
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

    def test_thumbs_down_clicked(self):
        # Prepare request object
        request = self.factory.get('/thumbsDownClicked?title=Carnegie%20Mellon')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Same as making a GET request to '/thumbsDownClicked')
        response = thumbs_down_clicked(request)
       
        # Checks to see if the data object has been updated properly    
        self.assertEqual(AnswerResource.objects.all().filter(title="Carnegie Mellon").first().thumbsDowns, 1)

        # Doing it again for redundancy
        response = thumbs_down_clicked(request)
        self.assertEqual(AnswerResource.objects.all().filter(title="Carnegie Mellon").first().thumbsDowns, 2)

    def test_resource_appeared(self):
        # Prepare request object
        request = self.factory.get('/resourceAppeared?title=Carnegie%20Mellon')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Same as making a GET request to '/resourceAppeared')
        response = resource_appeared(request)
       
        # Checks to see if the data object has been updated properly    
        self.assertEqual(AnswerResource.objects.all().filter(title="Carnegie Mellon").first().appearances, 1)

        # Doing it again for redundancy
        response = resource_appeared(request)
        self.assertEqual(AnswerResource.objects.all().filter(title="Carnegie Mellon").first().appearances, 2)

    def test_resource_clicked(self):
        # Prepare request object
        request = self.factory.get('/resourceClicked?title=Carnegie%20Mellon')
        request.user = self.user
        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Same as making a GET request to '/resourceClicked')
        response = resource_clicked(request)
       
        # Checks to see if the data object has been updated properly    
        self.assertEqual(AnswerResource.objects.all().filter(title="Carnegie Mellon").first().clicks, 1)

        # Doing it again for redundancy
        response = resource_clicked(request)
        self.assertEqual(AnswerResource.objects.all().filter(title="Carnegie Mellon").first().clicks, 2)

    