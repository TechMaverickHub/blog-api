from django.contrib.auth import get_user_model
from django.db import models

from app.article.models import BlogPost


# Create your models here.
class Like(models.Model):
    """Model for blog post likes"""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_likes',
        related_query_name='user_like'
    )

    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='post_likes',
        related_query_name='post_like'
    )

    # Additional field declarations
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'blog_post')