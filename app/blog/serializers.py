from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from app.blog.models import BlogPost
from app.category.models import Category


class BlogPostCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    user = serializers.UUIDField(write_only=True)
    category = serializers.UUIDField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'category', 'title', 'content', 'excerpt', 'image', 'tags', 'user'
        ]

    def create(self, validated_data):
        """Override create to convert UUIDs to model instances"""
        # Get the actual user and category instances
        user_id = validated_data.pop('user')
        category_id = validated_data.pop('category')

        User = get_user_model()
        user_instance = User.objects.get(pk=user_id,is_active=True)
        category_instance = Category.objects.get(pk=category_id,is_active=True)

        # Create the blog post with actual instances
        blog_post = BlogPost.objects.create(
            user=user_instance,
            category=category_instance,
            **validated_data
        )

        return blog_post

