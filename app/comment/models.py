from django.db import models

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_comments',
        related_query_name='user_comment'
    )
    blog_post = models.ForeignKey(
        'article.BlogPost',
        on_delete=models.CASCADE,
        related_name='post_comments',
        related_query_name='post_comment'
    )
    content = models.TextField()

    # Additional field declarations
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)