from django.shortcuts import render
from blog.models import Post
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from blog.forms import UserRegisterForm


class UserLogin(LoginView):
    template_name = 'blog/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('blog-home')

# Create your views here.
def home(request):
    post = Post.objects.all()
    return render(request, 'blog/home.html',{'posts':post})

def about(request):
    return render(request, 'blog/about.html')

class RegisterPage(FormView):
    template_name = 'blog/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.save()
        return super(RegisterPage, self).form_valid(form)