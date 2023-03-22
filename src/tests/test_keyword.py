from helpdesk_app.forms import ResourceForm
from helpdesk_app.models import AnswerResource
from django.test import TestCase

class KeywordTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test resource object for all test methods
        form_data = {
            'title' : "Check if scam website",
            'url' : "https://www.hbc.bank/11-ways-to-check-if-a-website-is-legit-or-trying-to-scam-you/", 
            'blurb' : "This resource gives 11 ways to determine if a website is legit or a scam", 
            'tags': "hbc, hbc bank, 11 ways, scam, legit"
        }
        form = ResourceForm(data=form_data)
        form.save()

    def test_object_valid(self):
        # Ensure the test object was successfully created
        record = AnswerResource.objects.get(id=1)
        self.assertIsNotNone(record)
        self.assertEqual(record.title, "Check if scam website")

    def test_keywords_created(self):
        record = AnswerResource.objects.get(id=1)
        # The record should have 5 tags
        tags = list(record.tags.names())
        self.assertEqual(len(tags), 5)
        # Check contents are the same as what was passed
        # (first sorting alphabetically)
        self.assertEqual(sorted(tags), ["11 ways", "hbc", "hbc bank", "legit", "scam"])

    def test_new_tag(self):
        record = AnswerResource.objects.get(id=1)
        # Currently has 5
        self.assertEqual(len(record.tags.names()), 5)
        # If we add a new one, it should now have 6
        record.tags.add("new tag")
        self.assertEqual(len(record.tags.names()), 6)

