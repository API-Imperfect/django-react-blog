import uuid

from autoslug import AutoSlugField
from blog.settings.base import AUTH_USER_MODEL
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel


class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PostPublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )


class Post(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, blank=False, editable=False
    )
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=255)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    content = models.TextField(_("Post Conten"))
    published_status = models.BooleanField(_("Published Status"), default=False)

    objects = models.Manager()
    published = PostPublishedManager()

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        """The title method returns a string where the first character in every word is upper case"""
        self.title = str.title(self.title)
        self.content = str.capitalize(self.content)
        super(Post, self).save(*args, **kwargs)
