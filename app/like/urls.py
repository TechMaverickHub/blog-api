from django.urls import path

from app.like.views import LikeCreateAPIView
from app.tag.views import TagCreateAPIView, TagDetailAPIView, TagListFilterAPIView

urlpatterns = [

    path("", LikeCreateAPIView.as_view(),name="like-create"),

]
