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
    path('home', views.search, name='home'),
    path('search', views.search, name='search'),
    path('signup/', views.signup, name="signup"),
    path('accounts/', views.accounts, name="accounts"),
    path('account', views.account_redirect, name="account_redirect"),
    path('account/<int:id>', views.account, name="account"),
    path('update_profile/<int:id>', views.update_profile, name="update_profile"),
    path('update_account/', views.update_account, name="update_account"),
]
