from datetime import datetime, timezone

from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'newnews.html'
    context_object_name = 'post'