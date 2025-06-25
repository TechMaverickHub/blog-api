from django.urls import path

from app.article.views import BlogCreateAPIView, BlogDetailAPIView, BlogListFilterAPIView, PostCommentListFilterAPIView

urlpatterns = [

    path("", BlogCreateAPIView.as_view(), name="blog-create"),
    path('<int:pk>', BlogDetailAPIView.as_view(), name='blog-detail'),
    path('list-filter/', BlogListFilterAPIView.as_view(), name='blog-list-filter'),


    # comment of post
    path('/comment/', PostCommentListFilterAPIView.as_view(), name='post-comment-detail'),

]
