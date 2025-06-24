from django.urls import path

from app.comment.views import CommentCreateAPIView

urlpatterns = [

    path("", CommentCreateAPIView.as_view(),name="post-create"),

]
