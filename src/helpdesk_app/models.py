from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from taggit.managers import TaggableManager
from picklefield.fields import PickledObjectField


# Profile for user model (helpdesk staff)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(
        max_length=5000,
        blank=True,
        default='',
        null=False
    )


# Model to represent categories
class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.category_name


# Model to represent resources
class AnswerResource(models.Model):
    # Short title to describe the resource (required)
    title = models.CharField(max_length=75, blank=False, null=False)
    # URL associated with the resource (required, must be unique)
    url = models.URLField(max_length=1000, unique=True, blank=False, null=False)
    # Blurb to describe the resource (required)
    blurb = models.CharField(max_length=2500, blank=True, default='')
    # Last updated
    updated = models.DateTimeField(auto_now=True)
    # Tagging
    tags = TaggableManager(help_text='Related keywords for this resource', blank=True)
    # Websraping content
    content = models.TextField(blank=True, default='')
    # Categories
    categories = models.ManyToManyField(Category)


# Model to represent queries
class Query(models.Model):
    raw_query = models.TextField(blank=False, null=False)
    processed_query = models.TextField(blank=False, null=False)
    encoded_query = PickledObjectField(null=True)
    occurrences = models.IntegerField()
    # Category the query was a part of
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
