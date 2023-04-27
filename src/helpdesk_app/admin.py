'''
This file concerns the default Django administration backend. This is different
from the "Admin Panel" which is a user-friendly interface to manage the application.
The Django backend allows more exhaustive and potentially dangerous control over the
system. You can navigate to it by going to `<url>/admin`.
'''
from django.contrib import admin
from .models import Profile, AnswerResource, Category
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(AnswerResource)
admin.site.register(Category)
