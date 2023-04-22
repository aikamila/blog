from django.db import models
from django.conf import settings


class CommonInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    time = models.DateTimeField(verbose_name="Time of posting")

    class Meta:
        abstract = True


class Post(CommonInfo):
    GENERAL = "GE"
    TECHNOLOGY = "TE"
    BEAUTY = "BE"
    FASHION = "FA"
    AGONY_AUNT = "AG"
    CATEGORY_CHOICES = [
        (GENERAL, "General"),
        (TECHNOLOGY, "Technology"),
        (BEAUTY, "Beauty"),
        (FASHION, "Fashion"),
        (AGONY_AUNT, "Agony Aunt"),
    ]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=GENERAL)
    engagement_rate = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)
    image = models.FileField(null=True, blank=True, upload_to="images/")

    class Meta:
        ordering = ['-time']


class Comment(CommonInfo):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ['time']


class Reply(CommonInfo):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")

    class Meta:
        ordering = ['time']
