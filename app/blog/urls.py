from django.urls import path

from app.blog.views import BlogCreateAPIView, BlogDetailAPI

urlpatterns = [

    path("", BlogCreateAPIView.as_view(), name="post-create"),
    path('<str:pk>', BlogDetailAPI.as_view(), name='post-detail'),
    # path('list-filter/', CategoryListFilterAPIView.as_view(), name='post-list-filter'),

]
