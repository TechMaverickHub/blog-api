from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.global_constants import SuccessMessage, ErrorMessage
from app.like.models import Like
from app.like.serializers import LikeCreateSerializer
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class LikeCreateAPIView(GenericAPIView):
    permission_classes = [IsUser]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'blog_post': openapi.Schema(type=openapi.TYPE_INTEGER, description='Post ID'),
            }
        )
    )
    def post(self, request):
        request.data['user'] = request.user.id

        # Check if the like already exists
        like_queryset = Like.objects.filter(blog_post_id=request.data['blog_post'], user_id=request.user.id).exists()

        if like_queryset:
            return get_response_schema(
                {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.POST_ALREADY_LIKE.value]},
                ErrorMessage.BAD_REQUEST.value,
                status.HTTP_400_BAD_REQUEST
            )



        serializer = LikeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return get_response_schema(
                serializer.data,
                SuccessMessage.RECORD_CREATED.value,
                status.HTTP_201_CREATED
            )
        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)
