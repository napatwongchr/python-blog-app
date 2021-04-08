from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<str:post_id>', views.single_post_detail, name='single_post_detail'),
    path('<str:post_id>/comments', views.comment_list, name='comment_list')
]