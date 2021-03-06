"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from blog.views import HomeList, PostCreate, PostDelete, PostDetail, PostUpdate, RegisterPage, UserLogin, UserPostList
from django.contrib.auth.views import LogoutView # PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout'),
    path('', HomeList.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostList.as_view(), name = 'user-posts'),
    path('register/', RegisterPage.as_view(), name = 'register'),
    path('profile/', views.Profile, name ='profile'),
    path('edit/', views.ProfileUpdate, name = 'edit'),
    path('detail/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('create/', PostCreate.as_view(), name = 'post-create'),
    path('detail/<int:pk>/update/', PostUpdate.as_view(), name = 'post-update'),
    path('detail/<int:pk>/delete/', PostDelete.as_view(), name = 'post-delete'), 

    #password Reset Modules:
    #Display a password reset form which ask you to enter email address:
    
    path('password-reset/', 
    auth_views.PasswordResetView.as_view(
        template_name='blog/password_reset.html'), 
        name='password_reset'),

    path('password-reset/done/', 
    auth_views.PasswordResetDoneView.as_view(
        template_name='blog/password_reset_done.html'), 
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(
         template_name='blog/password_reset_confirm.html'
         ),
          name='password_reset_confirm'),

    path('password-reset-complete/', 
    auth_views.PasswordResetCompleteView.as_view(
        template_name = 'blog/password_reset_complete.html'
        ), 
        name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
