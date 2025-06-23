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

class BlogDisplaySerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    category = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = (
            'title', 'content', 'excerpt', 'image', 'status',
            'tags', 'category', 'user', 'created', 'modified'
        )

    def get_category(self, obj):
        return obj.category.name if obj.category else None

    def get_user(self, obj):
        return obj.user.first_name + " " + obj.user.last_name


class BlogUpdateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    category = serializers.UUIDField(required=False)

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'excerpt', 'image', 'tags', 'status', 'category')

    def validate_title(self, value):
        return value.strip().capitalize()

    def validate_category(self, value):
        try:
            category = Category.objects.get(pk=value, is_active=True)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive category")
        return value

    def update(self, instance, validated_data):
        # Category resolution
        if 'category' in validated_data:
            category_id = validated_data.pop('category')
            instance.category = Category.objects.get(pk=category_id, is_active=True)

        # Tags update
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(*tags)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)

        instance.save()
        return instance
