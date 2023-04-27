'''
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/

Please note that there are two files: `helpdesk_app/urls.py` and `helpdesk_proj/urls.py`.
The `urls.py` in `helpdesk_app` are for URLs that are specific to the context of our application,
for example creating a new resource, updating a resource, creating a new category, and so forth.
On the other hand, the `urls.py` in `helpdesk_proj` are more project-focused and higher-level, e.g.
Rosetta or the Django administration backend.

The URLs defined in this file are automatically included (inherited) from the parent `urls.py` file
in `helpdesk_proj`. Given a technical limitation, it is important to note that URLs subject to internationalization
(for now, only the `search/` pages) are included as part of the parent file instead of this file.
'''
from django.urls import path
from helpdesk_app import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('search/', permanent=False), name='home'),
    path('autocomplete', views.autocomplete_search, name='autocomplete'),
    path('signup/', views.signup, name="signup"),
    path('accounts/', views.accounts, name="accounts"),
    path('account', views.account_redirect, name="account_redirect"),
    path('account/<int:id>', views.account, name="account"),
    path('update_profile/<int:id>', views.update_profile,
         name="update_profile"
         ),
    path('update_account/', views.update_account, name="update_account"),
    path('new_resource/', views.new_resource, name="new_resource"),
    path('update_resource/<int:id>', views.update_resource, name="update_resource"),
    path('delete_resource/<int:id>', views.delete_resource, name="delete_resource"),
    path('resources/', views.view_resources, name="resources"),
    path('new_category/', views.new_category, name="new_category"),
    path('update_category/<int:id>', views.update_category, name="update_category"),
    path('delete_category/<int:id>', views.delete_category, name="delete_category"),
    path('categories/', views.view_categories, name="categories"),
    path('get_faq', views.get_faq, name="get_faq"),
]
