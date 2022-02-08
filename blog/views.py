from django.shortcuts import render, redirect
from blog.models import Post, Profile
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from blog.forms import UserRegisterForm


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

@login_required
def Profile(request):
    return render(request,'blog/profile.html')


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