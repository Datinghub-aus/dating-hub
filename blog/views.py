# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost

def blog_index(request):
    """Main blog page with paginated posts"""
    # Get all published posts ordered by publication date
    posts_list = BlogPost.objects.filter(status='published')
    
    # Pagination - 9 posts per page
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories with post counts
    categories = []
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        count = BlogPost.objects.filter(
            status='published', 
            category=choice_value
        ).count()
        if count > 0:
            categories.append({
                'name': choice_label,
                'slug': choice_value,
                'post_count': count
            })
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(status='published')[:5]
    
    # Get featured posts (if you have this field, otherwise remove)
    featured_posts = BlogPost.objects.filter(status='published')[:3]
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'featured_posts': featured_posts,
        'title': 'Blog - Dating Hub Research',
    }
    return render(request, 'blog/index.html', context)

def blog_detail(request, slug):
    """Single blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts (same category, excluding current)
    related_posts = BlogPost.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(status='published').exclude(id=post.id)[:5]
    
    # Get categories for sidebar
    categories = []
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        count = BlogPost.objects.filter(
            status='published', 
            category=choice_value
        ).count()
        if count > 0:
            categories.append({
                'name': choice_label,
                'slug': choice_value,
                'post_count': count
            })
    
    # Get next and previous posts
    next_post = BlogPost.objects.filter(
        status='published',
        published_date__lt=post.published_date
    ).order_by('-published_date').first()
    
    prev_post = BlogPost.objects.filter(
        status='published',
        published_date__gt=post.published_date
    ).order_by('published_date').first()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'next_post': next_post,
        'prev_post': prev_post,
        'title': f'{post.title} - Blog - Dating Hub Research',
    }
    return render(request, 'blog/detail.html', context)

def blog_category(request, category_slug):
    """Posts filtered by category"""
    # Find the category label for the given slug
    category_label = None
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        if choice_value == category_slug:
            category_label = choice_label
            break
    
    if not category_label:
        # Return 404 if category not found
        from django.http import Http404
        raise Http404("Category not found")
    
    # Get posts in this category
    posts_list = BlogPost.objects.filter(
        category=category_slug,
        status='published'
    )
    
    # Pagination
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for sidebar
    categories = []
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        count = BlogPost.objects.filter(
            status='published', 
            category=choice_value
        ).count()
        if count > 0:
            categories.append({
                'name': choice_label,
                'slug': choice_value,
                'post_count': count
            })
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(status='published')[:5]
    
    context = {
        'category': {'slug': category_slug, 'name': category_label},
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'title': f'{category_label} - Blog - Dating Hub Research',
    }
    return render(request, 'blog/category.html', context)
