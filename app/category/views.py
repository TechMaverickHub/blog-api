import logging

from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.category.models import Category
from app.category.serializers import CategoryCreateSerializer, CategoryDisplaySerializer, \
    CategoryListFilterDisplaySerializer, CategoryUpdateSerializer
from app.core.views import CustomPageNumberPagination
from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema
from permissions import IsAdmin

logger = logging.getLogger('django')

# Create your views here.
class CategoryCreateAPIView(GenericAPIView):
    """ View: Create Category(Only )"""

    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of category'),
            }
        )
    )
    def post(self, request):
        with transaction.atomic():

            serializer = CategoryCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return get_response_schema(serializer.data,SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)

            return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPI(GenericAPIView):

    permission_classes = [IsAdmin]

    def get_object(self, pk):

        category_queryset = (Category.objects.filter(pk=pk,is_active=True)
                         .only('name'))
        if category_queryset:
            return category_queryset[0]
        return None

    def get(self, request, pk):

        logger.info(f"Category accessed by user: {request.user}. Requested user ID: {pk}")

        if not pk:
            logger.warning("Bad request: No primary key provided.")
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        category = self.get_object(pk)
        if not category:
            logger.error(f"Error retrieving category with ID {pk}", exc_info=True)
            return get_response_schema(
                {},
                ErrorMessage.NOT_FOUND.value,
                status.HTTP_404_NOT_FOUND
            )

        serializer = CategoryDisplaySerializer(category)
        logger.info(f"Successfully retrieved category with ID {pk}")
        return get_response_schema(
            serializer.data,
            SuccessMessage.RECORD_RETRIEVED.value,
            status.HTTP_200_OK
        )

    def delete(self, request, pk):

        logger.info(f"CategoryDetailAPI accessed by user: {request.user}. Requested user ID: {pk}")

        if not pk:
            logger.warning("Bad request: No primary key provided.")
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        category = self.get_object(pk)
        if not category:
            logger.error(f"Error retrieving Category with ID {pk}", exc_info=True)
            return get_response_schema(
                {},
                ErrorMessage.NOT_FOUND.value,
                status.HTTP_404_NOT_FOUND
            )

        category.is_active = False
        category.save()

        logger.info(f"Successfully deleted category with ID {pk}")

        return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of category'),
            }
        )
    )
    def put(self, request, pk):

        logger.info(f"CategoryDetailAPI accessed by user: {request.user}. Requested user ID: {pk}")

        if not pk:
            logger.warning("Bad request: No primary key provided.")
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        category = self.get_object(pk)
        if not category:
            logger.error(f"Error retrieving category with ID {pk}", exc_info=True)
            return get_response_schema(
                {},
                ErrorMessage.NOT_FOUND.value,
                status.HTTP_404_NOT_FOUND
            )

        serializer = CategoryUpdateSerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"Successfully updated category with ID {pk}")
            return get_response_schema(
                serializer.data,
                SuccessMessage.RECORD_UPDATED.value,
                status.HTTP_201_CREATED
            )

        logger.info(f"Error deleting category with ID {pk}")

        return get_response_schema(
            serializer.errors,
            ErrorMessage.BAD_REQUEST.value,
            status.HTTP_400_BAD_REQUEST
        )

class CategoryListFilterAPIView(ListAPIView):
    """ View: Post List Filter"""

    serializer_class = CategoryListFilterDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get_queryset(self):

        query_params = self.request.query_params

        # Only fetch necessary fields to optimize performance
        queryset = Category.objects.filter(
            is_active=True,
        ).only(
            'pk','name'
        ).order_by('-created')

        # Extract filters
        name = query_params.get('name')

        # Apply filters
        if name:
            queryset = queryset.filter(name__istartswith=name)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Filter by name of category'),

        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)