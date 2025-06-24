from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.category.models import Category
from app.tag.models import Tag


# Create your models here.
class BlogPost(models.Model):
    """Main blog post model"""

    # ENUM Choices
    class StatusChoice(models.TextChoices):
        DRAFT = "Draft", _("Draft")
        PUBLISHED = "Accepted", _("Accepted")

    # Key declarations
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_blog_posts',
        related_query_name='user_blog_post'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_blog_posts',
        related_query_name='category_blog_post')

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='tagged_blog_posts',
        related_query_name='tagged_blog_post'
    )

    # Field Declaration
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    status = models.CharField(max_length=10, choices=StatusChoice, default=StatusChoice.DRAFT.value)
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

    # Additional field declarations
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']
