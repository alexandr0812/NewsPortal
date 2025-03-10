from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.urls import reverse_lazy


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'newnews.html'
    context_object_name = 'post'

class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post_search'
    ordering = '-created_at'
    filter_class = PostFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=queryset)
        return self.filter.qs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        context['list_in_page'] = self.paginate_by
        context['all_posts'] = Post.objects.all()
        return context

class CreatePost(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save()
        id = post.id
        return redirect(f'/news/{id}')

class EditPost(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit_post.html'

class DeletePost(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    queryset = Post.objects.all()
    success_url = '/news/'