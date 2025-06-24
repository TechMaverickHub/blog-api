from django.db import models

# Create your models here.
class Tag(models.Model):
    """Tag Model"""

    name = models.CharField(max_length=100, unique=True)

    # Additional field declarations
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)