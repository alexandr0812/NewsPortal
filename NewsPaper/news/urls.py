from django.urls import path
from .views import PostsList, PostDetail, Search, CreatePost, EditPost, DeletePost

urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>/', PostDetail.as_view()),
   path('search/', Search.as_view()),
   path('create/', CreatePost.as_view()),
   path('<int:pk>/edit', EditPost.as_view()),
   path('<int:pk>/delete', DeletePost.as_view()),
]