from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


# Profile for user model (helpdesk staff)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(
        max_length=5000,
        blank=True,
        default='',
        null=False
    )


# Model to represent resources
class AnswerResource(models.Model):
    # Short title to describe the resource (required)
    title = models.CharField(max_length=100, blank=False, null=False)
    # URL associated with the resource (required, must be unique)
    url = models.URLField(max_length=1000, unique=True, blank=False, null=False)
    # Blurb to describe the resource (required)
    blurb = models.CharField(max_length=2500, blank=True, default='')
    # Last updated
    updated = models.DateTimeField(auto_now=True)


# Model to represen a keyword (resources can have many keywords)
class Keyword(models.Model):
    # The resource this keyword belongs to
    # If the resource gets deleted, all keywords will be deleted as well (CASCADE)
    resource = models.ForeignKey(AnswerResource, on_delete=models.CASCADE, blank=True, null=True)
    # Short word or phrase to describe the keyword
    name = models.CharField(max_length=100, blank=False, null=False)
    # Last updated
    updated = models.DateTimeField(auto_now=True)


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
