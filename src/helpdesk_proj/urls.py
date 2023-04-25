"""helpdesk_proj URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from helpdesk_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns

# Project-level URLs (e.g. admin panel, rosetta)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("rosetta/", include('rosetta.urls')),
    path("", include("django.contrib.auth.urls")),
    # All application-level URLs (e.g. adding new resources, categories) are included here
    path("", include("helpdesk_app.urls")),
]

# URLs that are subject to translation
# (for now, only the search page as that's the only page that non-employees can see)
urlpatterns += i18n_patterns(
    path("search/", views.search, name="search"),
    path('search/thumbsUpClicked', views.thumbs_up_clicked, name='thumbsUpClicked'),
    path('search/resourceClicked', views.resource_clicked, name='resourceClicked'),
    path('search/resourceAppeared', views.resource_appeared, name='resourceAppeared'),
)

urlpatterns += staticfiles_urlpatterns()
