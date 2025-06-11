import uuid

from django.db import models

# Create your models here.
class Category(models.Model):
    """Blog post categories like 'Tech', 'Life', 'Travel'"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    # Additional field declarations
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
