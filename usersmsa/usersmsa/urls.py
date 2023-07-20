"""
URL configuration for usersmsa project.

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

from uit_users.views import UserView
from .service.views import PostsListView, PostsAuthorListView, PostsWithAuthorsListView, PostAuthorView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', UserView.as_view()),   # 1
    path('posts', PostsListView.as_view()),  # 2
    path('authors/<int:user_id>/posts', PostsAuthorListView.as_view()),   # 3
    path('posts/<int:post_id>', PostAuthorView.as_view()),   # 4
    path('authors/posts', PostsWithAuthorsListView.as_view()),   # 5
]
