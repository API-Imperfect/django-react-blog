import logging

from blog.settings.base import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profiles.models import UserProfile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    logger.info(f"{instance}'s profile created successfully")
