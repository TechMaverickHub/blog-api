from rest_framework import serializers

from app.like.models import Like


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('blog_post', 'user')