from django.urls import path
from .views import PostsListView, PostCreateView


app_name = 'posts'

urlpatterns = [
    path('', PostsListView.as_view(), name="list"),
    path('new-post/', PostCreateView.as_view(), name="new-post"),
]
