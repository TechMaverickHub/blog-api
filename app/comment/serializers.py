from rest_framework import serializers

from app.comment.models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'blog_post', 'content')