from helpdesk_app.views import search, new_resource
from helpdesk_app.models import AnswerResource, Category
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils import translation

class InternationalizationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Mock translation strings to ensure tests don't fail in prod
        translation_catalog = translation.trans_real.translation("es")
        translation_catalog._catalog['Category search'] = 'Categoría'
        translation_catalog._catalog['Search'] = 'Buscar'

    def test_homepage_english(self):
        request = self.factory.get('/search/')
        response = search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        
        # Ensure the "Search" button is in English
        self.assertNotEqual(decoded_response.find("Search"), -1)
        # Ensure the "Search" button is NOT in Spanish
        self.assertEquals(decoded_response.find("Buscar"), -1)

    def test_homepage_spanish(self):
        # Set locale to Spanish
        translation.activate('es')
        request = self.factory.get('/search/') # Will automatically redirect to /es/

        # Necessary as messages and session middleware are not instantiated in test environments
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        
        response = search(request)
        decoded_response = str(response.content.decode('utf-8').rstrip().split('\n'))
        
        # Ensure the "Search" button is in Spanish
        self.assertNotEqual(decoded_response.find("Buscar"), -1)
        # Ensure no English elements
        self.assertEquals(decoded_response.find("Category search"), -1)

        # Reset back to English
        translation.activate('en')
