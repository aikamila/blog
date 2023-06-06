from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
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
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=GENERAL)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_list')

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.post.pk])

