from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.comment.serializers import CommentCreateSerializer
from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class CommentCreateAPIView(GenericAPIView):

    permission_classes = [IsUser]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'blog_post': openapi.Schema(type=openapi.TYPE_INTEGER, description='Blog post id'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Comment'),
            }
        )
    )
    def post(self, request):

        request.data['user'] = request.user.id

        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data,SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)

        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

