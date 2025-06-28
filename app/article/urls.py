from django.urls import path

from app.article.views import BlogCreateAPIView, BlogDetailAPIView, BlogListFilterAPIView

urlpatterns = [

    path("", BlogCreateAPIView.as_view(), name="blog-create"),
    path('<int:pk>', BlogDetailAPIView.as_view(), name='blog-detail'),
    path('list-filter/', BlogListFilterAPIView.as_view(), name='blog-list-filter'),

]
