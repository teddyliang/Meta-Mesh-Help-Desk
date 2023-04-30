'''
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/

Please note that there are two files: `helpdesk_app/urls.py` and `helpdesk_proj/urls.py`.
The `urls.py` in `helpdesk_app` are for URLs that are specific to the context of our application,
for example creating a new resource, updating a resource, creating a new category, and so forth.
On the other hand, the `urls.py` in `helpdesk_proj` (this file) are more project-focused and higher-level,
e.g. Rosetta or the Django administration backend.

The URLs defined in `helpdesk_app/urls.py` file are automatically included (inherited) in this parent file.
Given a technical limitation, it is important to note that URLs subject to internationalization
(for now, only the `search/` pages) are included as part of this parent file instead of the `app` file.
'''
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
    # Authentication URLs
    path("", include("django.contrib.auth.urls")),
    # All application-level URLs (e.g. adding new resources, categories) are included here
    path("", include("helpdesk_app.urls")),
]

# URLs that are subject to translation
# (for now, only the search page as that's the only page that non-employees can see)
urlpatterns += i18n_patterns(
    path("search/", views.search, name="search"),
    path('search/thumbsDownClicked', views.thumbs_down_clicked, name='thumbsDownClicked'),
    path('search/resourceClicked', views.resource_clicked, name='resourceClicked'),
    path('search/resourceAppeared', views.resource_appeared, name='resourceAppeared'),
)

urlpatterns += staticfiles_urlpatterns()
