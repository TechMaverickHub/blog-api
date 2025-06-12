import uuid

from django.conf import settings
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.blog.serializers import BlogPostCreateSerializer
from app.category.models import Category
from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema
from permissions import IsUser


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
