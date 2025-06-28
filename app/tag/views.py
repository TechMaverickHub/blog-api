from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.core.views import CustomPageNumberPagination
from app.global_constants import SuccessMessage, ErrorMessage
from app.tag.models import Tag
from app.tag.serializers import TagCreateSerializer, TagDisplaySerializer, TagUpdateSerializer
from app.utils import get_response_schema
from permissions import IsAdmin


# Create your views here.
class TagCreateAPIView(GenericAPIView):
    """View: Create Tag(Only Admin can create)"""

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

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
            serializer = TagCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return get_response_schema(serializer.data, SuccessMessage.RECORD_CREATED.value,
                                           status.HTTP_201_CREATED)

            return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class TagDetailAPIView(GenericAPIView):
    """View: Read, Update, Delete Tag(Only Admin)"""

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):

        tag_queryset = Tag.objects.filter(pk=pk, is_active=True)

        if tag_queryset.exists():
            return tag_queryset.first()

        return None

    def get(self, request, pk):

        if not pk:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


        tag = self.get_object(pk)

        if not tag:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = TagDisplaySerializer(tag)

        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of category'),
            }
        )
    )
    def put(self, request, pk):

        if not pk:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        tag = self.get_object(pk)

        if not tag:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = TagUpdateSerializer(tag, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)

        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):

        if not pk:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        tag = self.get_object(pk)

        if not tag:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        tag.is_active = False
        tag.save()

        return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)


class TagListFilterAPIView(ListAPIView):
    """View: List Filter ag(Only Admin)"""

    serializer_class = TagDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get_queryset(self):

        queryset = Tag.objects.filter(is_active=True).order_by('-created')

        # Filter by name
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING,)
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)







