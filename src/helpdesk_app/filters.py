import django_filters
from django_filters import OrderingFilter
from .models import User


class UserFilter(django_filters.FilterSet):
    # Ordering
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
        super(UserFilter, self).__init__(*args, **kwargs)
        self.filters['is_superuser'].label = "Superadmin status:"
