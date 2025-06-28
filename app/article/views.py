import logging
import uuid

from django.conf import settings
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.article.models import BlogPost
from app.article.serializers import BlogPostCreateSerializer, BlogPostDisplaySerializer, BlogPostUpdateSerializer
from app.category.models import Category
from app.core.views import CustomPageNumberPagination
from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema
from permissions import IsUser

logger = logging.getLogger('django')


# Create your views here.
class BlogCreateAPIView(GenericAPIView):
    """View: Create Blog Post (Admin Only)"""

    permission_classes = [IsUser]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the blog'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the blog'),
                'excerpt': openapi.Schema(type=openapi.TYPE_STRING, description='Excerpt'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Image file'),
                'tags': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description='List of tags'
                )
            }
        )
    )
    def post(self, request):
        with transaction.atomic():
            request.data['user'] = request.user.id

            serializer = BlogPostCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return get_response_schema(
                    serializer.data,
                    SuccessMessage.RECORD_CREATED.value,
                    status.HTTP_201_CREATED
                )

            return get_response_schema(
                serializer.errors,
                ErrorMessage.BAD_REQUEST.value,
                status.HTTP_400_BAD_REQUEST
            )


class BlogDetailAPIView(GenericAPIView):
    """View: Read, Update, Delete Blog Post(User Only)"""

    permission_classes = [IsUser]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):

        blog_queryset = BlogPost.objects.filter(pk=pk, is_active=True)

        if blog_queryset:
            return blog_queryset[0]
        return None

    def get(self, request, pk):

        if not pk:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        blog = self.get_object(pk)

        if not blog:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = BlogPostDisplaySerializer(blog)

        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the blog'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the blog'),
                'excerpt': openapi.Schema(type=openapi.TYPE_STRING, description='Excerpt'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Image file'),
                'tags': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description='List of tags'
                )
            }
        )
    )
    def put(self, request, pk):

        if not pk:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        blog = self.get_object(pk)

        if not blog:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = BlogPostUpdateSerializer(blog, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)

        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        if not pk:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        blog = self.get_object(pk)

        if not blog:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        blog.is_active = False
        blog.save()

        return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)


class BlogListFilterAPIView(ListAPIView):
    """View: Blog List Filter(Only User)"""

    permission_classes = [IsUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = BlogPostDisplaySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):

        blog_queryset = self.request.user.user_blog_posts.filter(is_active=True)

        # Filter by title
        title = self.request.query_params.get('title')
        if title is not None:
            blog_queryset = blog_queryset.filter(title__icontains=title)

        # Filter by category
        category = self.request.query_params.get('category')
        if category is not None:
            blog_queryset = blog_queryset.filter(category=category)

        # Filter by multiple tags
        tags_list = self.request.query_params.getlist('tags')
        if tags_list is not None:
            tag_ids = [tag for tag in tags_list]
            if tag_ids:
                blog_queryset = blog_queryset.filter(tags__in=tag_ids).distinct()

        # Filter by status
        status = self.request.query_params.get('status')
        if status is not None:
            blog_queryset = blog_queryset.filter(status=status)

        return blog_queryset
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Title'),
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Category'),
            openapi.Parameter('tags', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Tags'),
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=[choice[0] for choice in BlogPost.StatusChoice.choices], description='Status'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





