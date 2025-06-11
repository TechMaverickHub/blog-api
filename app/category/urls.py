from django.urls import path

from app.category.views import CategoryCreateAPIView, CategoryListFilterAPIView, CategoryDetailAPI

urlpatterns = [

    path("", CategoryCreateAPIView.as_view(),name="post-create"),
    path('<str:pk>', CategoryDetailAPI.as_view(), name='post-detail'),
    path('list-filter/', CategoryListFilterAPIView.as_view(), name='post-list-filter'),

]
