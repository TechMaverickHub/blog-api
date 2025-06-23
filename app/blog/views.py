import logging
import uuid

from django.conf import settings
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.blog.models import BlogPost
from app.blog.serializers import BlogPostCreateSerializer, BlogDisplaySerializer, BlogUpdateSerializer
from app.category.models import Category
from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema
from permissions import IsUser

logger = logging.getLogger('django')

# Create your views here.
class BlogCreateAPIView(GenericAPIView):
    """View: Create Blog Post (Admin Only)"""

    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={
                'category': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Category ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the blog'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the blog'),
                'excerpt': openapi.Schema(type=openapi.TYPE_STRING, description='Excerpt'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Image file'),
                'tags': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description='List of tags'
                )
            }
        )
    )
    def post(self, request):
        with transaction.atomic():
            request.data['user'] = str(request.user.id)

            category = request.data.pop('category')

            # verify the category exists
            category_obj = Category.objects.only('name').filter(pk=uuid.UUID(category),is_active=True)
            if not category_obj.exists():
                return_data = {
                    settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [
                        ErrorMessage.CATEGORY_NOT_FOUND.value]
                }
                return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value,
                                           status.HTTP_400_BAD_REQUEST)

            request.data['category'] = category
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


class BlogDetailAPI(GenericAPIView):
    """View: Retrieve, Update, and Delete BlogPost (Admin Only)"""

    permission_classes = [IsUser]

    def get_object(self, pk):
        blog_queryset = BlogPost.objects.filter(pk=pk, is_active=True)
        if blog_queryset.exists():
            return blog_queryset.first()
        return None

    def get(self, request, pk):
        logger.info(f"BlogDetailAPI GET accessed by user: {request.user}. Blog ID: {pk}")

        if not pk:
            logger.warning("Bad request: No primary key provided.")
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        blog = self.get_object(pk)
        if not blog:
            logger.error(f"Blog with ID {pk} not found.")
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = BlogDisplaySerializer(blog)
        logger.info(f"Successfully retrieved blog with ID {pk}")
        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

    def delete(self, request, pk):
        logger.info(f"BlogDetailAPI DELETE accessed by user: {request.user}. Blog ID: {pk}")

        if not pk:
            logger.warning("Bad request: No primary key provided.")
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        blog = self.get_object(pk)
        if not blog:
            logger.error(f"Blog with ID {pk} not found.")
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        blog.is_active = False
        blog.save()

        logger.info(f"Successfully soft-deleted blog with ID {pk}")
        return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the blog'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the blog'),
                'excerpt': openapi.Schema(type=openapi.TYPE_STRING, description='Excerpt of the blog'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image URL or path'),
                'tags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['draft', 'published']),
                'category': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Category ID'),
            }
        )
    )
    def put(self, request, pk):
        logger.info(f"BlogDetailAPI PUT accessed by user: {request.user}. Blog ID: {pk}")

        if not pk:
            logger.warning("Bad request: No primary key provided.")
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        blog = self.get_object(pk)
        if not blog:
            logger.error(f"Blog with ID {pk} not found.")
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = BlogUpdateSerializer(blog, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"Successfully updated blog with ID {pk}")
            return get_response_schema(serializer.data, SuccessMessage.RECORD_UPDATED.value, status.HTTP_201_CREATED)

        logger.error(f"Validation failed for blog update with ID {pk}: {serializer.errors}")
        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)