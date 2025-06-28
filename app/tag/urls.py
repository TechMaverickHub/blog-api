from django.urls import path

from app.tag.views import TagCreateAPIView, TagDetailAPIView, TagListFilterAPIView

urlpatterns = [

    path("", TagCreateAPIView.as_view(),name="tag-create"),
    path('<int:pk>', TagDetailAPIView.as_view(), name='tag-detail'),
    path('list-filter/', TagListFilterAPIView.as_view(), name='tag-list-filter'),

]
