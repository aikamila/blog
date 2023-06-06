from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.http import Http404


class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all()
        else:
            return Post.objects.filter(public=True)


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if (not self.request.user.is_authenticated) and (not object.public):
            raise Http404("Post does not exist")

        return super().dispatch(request, *args, **kwargs)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'image', 'public', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class PostSearch(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query_title = self.request.GET.get('qtitle')
        query_category = self.request.GET.get('qcategory')
        if query_title:
            ret_val = Post.objects.filter(title__icontains=query_title)
        else:
            ret_val = Post.objects.all()
        if query_category:
            ret_val = ret_val.filter(category=query_category)
        return ret_val

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options'] = Post.CATEGORY_CHOICES
        return context


class CustomLoginView(auth_views.LoginView):
    next_page = reverse_lazy('blog:post_list')


class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('blog:post_list')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def registration_success(request):
    return render(request, 'registration/registration_success.html')
