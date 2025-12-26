# blog/urls.py - UPDATED WITH TAG SUPPORT
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Main blog pages
    path('', views.blog_index, name='blog_index'),
    path('category/<str:category_slug>/', views.blog_category, name='blog_category'),
    path('tag/<slug:tag_slug>/', views.blog_tag, name='blog_tag'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # SEO sitemaps (you'll need to create these views)
    # path('sitemap.xml', views.blog_sitemap, name='blog_sitemap'),
    # path('feed/', views.blog_feed, name='blog_feed'),
]
