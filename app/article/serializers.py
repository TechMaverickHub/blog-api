from rest_framework import serializers

from app.article.models import BlogPost
from app.category.models import Category
from app.tag.models import Tag


class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = (
            'pk',
            'title',
            'content',
            'excerpt',
            'image',
            'category',
            'tags',
            'status',
            'user',
        )

    def validate_category(self, value):
        """Validate that category exists and is active"""
        if value and not Category.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Invalid category")
        return value

    def validate_tags(self, value):
        """Validate that all tags exist and are active"""
        if value:
            tag_ids = [tag.pk for tag in value]
            existing_tags = Tag.objects.filter(pk__in=tag_ids, is_active=True)
            if existing_tags.count() != len(tag_ids):
                raise serializers.ValidationError("One or more tags are invalid")
        return value


class BlogPostDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('pk',
                  'title',
                  'content',
                  'excerpt',
                  'image',
                  'category',
                  'tags',
                  'status',
                  'user',)
class BlogPostListFilterDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('pk',
                  'title',
                  'excerpt',
                  'image',
                  'category',
                  'tags',
                  'status',)


class BlogPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('pk',
                  'title',
                  'content',
                  'excerpt',
                  'image',
                  'category',
                  'tags',
                  'status',
                  'user',)

    def update(self, instance, validated_data):
        """Override update to handle tags replacement properly"""

        tags_data = validated_data.pop('tags', None)

        instance = super().update(instance, validated_data)

        # Handle tags replacement (only if tags are provided in the request)
        if tags_data is not None:
            # This will replace all existing tags with the new ones
            instance.tags.set(tags_data)


