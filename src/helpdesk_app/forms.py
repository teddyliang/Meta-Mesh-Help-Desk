from .models import Profile, AnswerResource, Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class NumberInput(forms.NumberInput):
    input_type = 'number'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Please provide a valid email address.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description',)


class ResourceForm(forms.ModelForm):
    class Meta:
        model = AnswerResource
        fields = ['title', 'url', 'blurb', 'tags', 'categories']

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'A short title describing the resource'
        self.fields['url'].label = 'A static URL associated with this resource that users will be directed to'
        self.fields['blurb'].label = 'A short blurb describing this resource'
        self.fields['tags'].label = 'Comma-separated list of keywords for this resource'
        self.fields['categories'].label = 'Associated categories (you may select multiple by holding CTRL)'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['category_name'].label = 'A short name for this category (ideally one word)'
