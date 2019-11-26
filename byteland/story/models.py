import pytz
from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from byteland.core.models import TimeStampedModel

from .utils import get_domain


class StoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Story(TimeStampedModel):
    objects = models.Manager()
    stories = StoryManager()

    title = models.CharField(_('title'), max_length=500)
    story_url = models.URLField(
        _('url'), max_length=2000, blank=True, null=True)
    story_body_text = models.TextField(
        _('sotry body text (use markdown)'), blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories'
    )
    deleted = models.BooleanField(default=False)
    number_of_comments = models.IntegerField(default=0)
    number_of_votes = models.IntegerField(default=0)
    url_domain_name = models.CharField(max_length=500, blank=True)
    rank = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def update_number_of_comments(self):
        self.number_of_comments = self.comments.count()
        self.save()

    def update_number_of_votes(self):
        self.number_of_votes = self.storypoint_set.count()
        self.save()

    def save(self, *args, **kwargs):
        if self.story_url:
            self.url_domain_name = get_domain(self.story_url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("story:show_story", args=[self.id])

    def calc_rank(self):
        """
        Rank = (P-1) / (T+2)^G
        """
        diff = datetime.utcnow().replace(tzinfo=pytz.utc) - self.created.togregorian()
        T = diff.total_seconds() / 60 / 60
        G = 1.8
        P = self.number_of_votes
        self.rank = P / pow((T+2), G)
        self.save()


class StoryComment(TimeStampedModel):
    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name='comments')
    story_comment = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.story_comment[:100]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the real save() method
        self.story.update_number_of_comments()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.story.update_number_of_comments()


class StoryPoint(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.story.update_number_of_votes()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.story.update_number_of_votes()
