from django.urls import path

from app.blog.views import BlogCreateAPIView

urlpatterns = [

    path("", BlogCreateAPIView.as_view(), name="post-create"),
    # path('<str:pk>', CategoryDetailAPI.as_view(), name='post-detail'),
    # path('list-filter/', CategoryListFilterAPIView.as_view(), name='post-list-filter'),

]
