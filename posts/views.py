from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import CreatePost


class PostsListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePost
    template_name = 'posts/post_new.html'
    login_url = '/users/login/'
    success_url = reverse_lazy('posts:list')

    def form_valid(self, form):
        newpost = form.save(commit=False)
        newpost.author = self.request.user
        newpost.save()
        return super().form_valid(form)
