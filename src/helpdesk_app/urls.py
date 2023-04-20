"""helpdesk_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from helpdesk_app import views

urlpatterns = [
    path('', views.search, name='home'),
    path('thumbsUpClicked', views.thumbsUpClicked, name='thumbsUpClicked'),
    path('resourceClicked', views.resourceClicked, name='resourceClicked'),
    path('resourceAppeared', views.resourceAppeared, name='resourceAppeared'),
    path('autocomplete', views.autocomplete_search, name='autocomplete'),
    path('home', views.search, name='home'),
    path('search', views.search, name='search'),
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
]
