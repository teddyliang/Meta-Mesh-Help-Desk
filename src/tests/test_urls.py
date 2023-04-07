from django.test import TestCase
from django.urls import resolve

class HomePageTest(TestCase):
    def test_root_url_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.view_name, 'home')

    def test_logged_user_home(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

class AutoCompleteTest(TestCase):
    def test_autcomplete_page_view(self):
        found = resolve('/autocomplete')
        self.assertEqual(found.view_name, 'autocomplete')
    def test_autocomplete_view(self):
        response = self.client.get('/autocomplete', follow=True)
        self.assertEqual(response.status_code, 200)
        
class AccountsPageTest(TestCase):
    def test_accounts_page_view(self):
        found = resolve('/accounts/')
        self.assertEqual(found.view_name, 'accounts')

    def test_logged_user_accounts(self):
        response = self.client.get('/accounts/', follow=True)
        self.assertEqual(response.status_code, 200)

class AccountPageTest(TestCase):
    def test_account_page_view(self):
        found = resolve('/account/1')
        self.assertEqual(found.view_name, 'account')

    def test_redirect_account_to_user_account(self):
        response = self.client.get('/account', follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)

class UpdateProfilePageTest(TestCase):
    def test_update_profile_page_view(self):
        found = resolve('/update_profile/1')
        self.assertEqual(found.view_name, 'update_profile')

    def test_logged_user_update_profile(self):
        response = self.client.get('/update_profile/1', follow=True)
        self.assertEqual(response.status_code, 200)

class UpdateAccountPageTest(TestCase):
    def test_update_account_page_view(self):
        found = resolve('/update_account/')
        self.assertEqual(found.view_name, 'update_account')

    def test_logged_user_update_profile(self):
        response = self.client.get('/update_account/', follow=True)
        self.assertEqual(response.status_code, 200)