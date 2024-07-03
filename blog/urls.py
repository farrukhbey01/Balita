from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('',home),
    path('blog/<int:pk>/', blog_detail, name = 'blog_detail'),
    # path('blog/', blog),
    path('about/', about),
    path('contact/', contact),
    path('category/', category),
    path('search/', search),
    path('tags/<int:pk>/', tags, name = 'tags'),


]