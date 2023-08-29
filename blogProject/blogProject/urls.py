"""
URL configuration for blogProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('blog/', views.blog),
    path('create/', views.create),
    path('show/<int:nid>', views.show),
    path('user/', views.user),
    path('user/add/', views.user_add),
    path('user/get/', views.user_get),
    path('user/edit/', views.user_edit),
    path('user/delete/', views.user_delete),
    path('blog/list/', views.blog_list),
    path('blog/get/', views.blog_get),
    path('blog/edit/', views.blog_edit),
    path('blog/delete/', views.blog_delete),


]
