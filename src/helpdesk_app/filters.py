'''
This file defines, for each model, all ways to filter
and order its results.
'''
import django_filters
from django_filters import DateFilter, OrderingFilter, CharFilter
from .models import Category, User, AnswerResource


class UserFilter(django_filters.FilterSet):
    # Ordering filters
    o = OrderingFilter(
        fields=(
            ('last_login', 'last_login'),
            ('date_joined', 'date_joined'),
            ('username', 'username'),
        ),
        field_labels={
            'last_login': 'Last login',
            'date_joined': 'Date account created',
            'username': 'Username',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'is_superuser']

    def __init__(self, *args, **kwargs):
        '''
        This is necessary in order to be able to change the displayed label for filters.
        '''
        super(UserFilter, self).__init__(*args, **kwargs)
        self.filters['is_superuser'].label = "Superadmin status:"


class ResourceFilter(django_filters.FilterSet):
    updated = DateFilter(field_name="updated", lookup_expr='gte')

    def keyword_search(queryset, name, value):
        '''
        Unfortunately, the default Django text filter is case sensitive and must completely match the string.
        Meaning, no results would be returned when searching for "dja" and expecting "django". Instead, we create
        a custom text-based filter that does this search which is case-insensitive and permits substrings.
        '''
        if value is not None:
            records = AnswerResource.objects.all()
            ids = [record.id for record in records
                   if value.lower() in str(record.blurb).lower() or value.lower() in str(record.title) or value.lower() in str(record.url)
                   ]
            return queryset.filter(id__in=ids)
        return queryset
    # Now define the custom text filter (the method it'll use is the above-defined method)
    keyword_search = CharFilter(method=keyword_search, label='Keyword search')

    # Ordering filters
    o = OrderingFilter(
        fields=(
            ('title', 'title'),
            ('url', 'url'),
            ('blurb', 'blurb')
        ),
        field_labels={
            'title': 'Title',
            'url': 'URL',
            'blurb': 'Blurb'
        }
    )

    class Meta:
        ordering = ['-updated']
        model = AnswerResource
        fields = ['updated', 'categories']

    def __init__(self, *args, **kwargs):
        '''
        This is necessary in order to be able to change the displayed label for filters.
        '''
        super(ResourceFilter, self).__init__(*args, **kwargs)
        self.filters['updated'].label = "Last updated date is on or after:"


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['category_name']
