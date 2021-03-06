from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from blog.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class UserLogin(LoginView):
    template_name = 'blog/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('blog-home')

class HomeList(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostList(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetail(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/Postcreate.html"
    #success_url = reverse_lazy('post-detail')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/Postcreate.html"
    #success_url = reverse_lazy('post-detail')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog-home')
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def Profile(request):
    return render(request,'blog/profile.html')

@login_required
def ProfileUpdate(request):
    if request.method == 'POST':
        P_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        U_form = UserUpdateForm(request.POST, instance= request.user)

        if P_form.is_valid() and U_form.is_valid():
            U_form.save()
            P_form.save()
            return redirect('profile')
    else:
        P_form = ProfileUpdateForm(instance=request.user.profile)
        U_form = UserUpdateForm(instance= request.user)
    return render(request,'blog/p_update.html', { 'U_form':U_form, 'P_form':P_form})


class RegisterPage(FormView):
    template_name = 'blog/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.save()
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blog-home')
        return super(RegisterPage, self).get (*args, **kwargs)