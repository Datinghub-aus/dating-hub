# blog/views.py - SEO OPTIMIZED
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import BlogPost, Tag

def blog_index(request):
    """Main blog page with paginated posts and SEO optimization"""
    posts_list = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).select_related().prefetch_related('tags')
    
    # Pagination - 9 posts per page (good for SEO with proper pagination)
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories with post counts for sidebar
    categories = []
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        count = BlogPost.objects.filter(
            status='published',
            published_date__lte=timezone.now(),
            category=choice_value
        ).count()
        if count > 0:
            categories.append({
                'name': choice_label,
                'slug': choice_value,
                'post_count': count
            })
    
    # Get popular tags (with at least 2 posts)
    popular_tags = Tag.objects.annotate(
        post_count=Count('blogpost')
    ).filter(post_count__gte=2).order_by('-post_count')[:10]
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).order_by('-published_date')[:5]
    
    # Get featured posts
    featured_posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now(),
        is_featured=True
    ).order_by('-published_date')[:3]
    
    # SEO Meta Data
    seo_data = {
        'title': 'Dating Hub Research Blog - Expert Insights & Advice',
        'meta_description': 'Explore research insights, dating trends, relationship psychology, and practical advice from Dating Hub Research Team. Stay updated with the latest in modern dating.',
        'meta_keywords': 'dating advice, relationship research, dating trends, modern dating, love psychology',
        'canonical_url': request.build_absolute_uri(request.path),
        'og_type': 'website',
    }
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'featured_posts': featured_posts,
        'seo': seo_data,
    }
    return render(request, 'blog/index.html', context)

def blog_detail(request, slug):
    """Single blog post detail view with full SEO optimization"""
    post = get_object_or_404(
        BlogPost.objects.select_related().prefetch_related('tags'),
        slug=slug,
        status='published',
        published_date__lte=timezone.now()
    )
    
    # Increment view count
    post.views += 1
    post.save(update_fields=['views'])
    
    # Get related posts (same category or tags, excluding current)
    related_posts = BlogPost.objects.filter(
        Q(category=post.category) | Q(tags__in=post.tags.all()),
        status='published',
        published_date__lte=timezone.now()
    ).exclude(id=post.id).distinct()[:4]
    
    # Get next and previous posts for better navigation
    next_post = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now(),
        published_date__gt=post.published_date
    ).order_by('published_date').first()
    
    prev_post = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now(),
        published_date__lt=post.published_date
    ).order_by('-published_date').first()
    
    # Get popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count('blogpost')
    ).filter(post_count__gte=2).order_by('-post_count')[:10]
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).exclude(id=post.id).order_by('-published_date')[:5]
    
    # SEO Meta Data
    seo_data = {
        'title': post.meta_title or post.title,
        'meta_description': post.meta_description or post.excerpt or post.content[:160],
        'meta_keywords': post.get_keywords(),
        'canonical_url': post.canonical_url or request.build_absolute_uri(post.get_absolute_url()),
        'og_type': 'article',
        'article_published_time': post.published_date.isoformat(),
        'article_modified_time': post.last_modified.isoformat(),
        'article_author': post.author,
        'article_section': post.get_category_display_name(),
        'og_image': post.featured_image.url if post.featured_image else None,
        'og_image_alt': post.featured_image_alt or post.title,
        'twitter_card': 'summary_large_image' if post.featured_image else 'summary',
    }
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'next_post': next_post,
        'prev_post': prev_post,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'seo': seo_data,
    }
    return render(request, 'blog/detail.html', context)

def blog_category(request, category_slug):
    """Posts filtered by category with SEO optimization"""
    # Find the category label for the given slug
    category_label = None
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        if choice_value == category_slug:
            category_label = choice_label
            break
    
    if not category_label:
        from django.http import Http404
        raise Http404("Category not found")
    
    # Get posts in this category
    posts_list = BlogPost.objects.filter(
        category=category_slug,
        status='published',
        published_date__lte=timezone.now()
    ).select_related().prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for sidebar
    categories = []
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        count = BlogPost.objects.filter(
            status='published',
            published_date__lte=timezone.now(),
            category=choice_value
        ).count()
        if count > 0:
            categories.append({
                'name': choice_label,
                'slug': choice_value,
                'post_count': count
            })
    
    # Get popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count('blogpost')
    ).filter(post_count__gte=2).order_by('-post_count')[:10]
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).order_by('-published_date')[:5]
    
    # SEO Meta Data
    seo_data = {
        'title': f'{category_label} - Dating Hub Research',
        'meta_description': f'Explore all {category_label.lower()} articles and research from Dating Hub Research Team. Expert insights on modern dating.',
        'meta_keywords': f'{category_label.lower()}, dating research, relationship advice, {category_slug}',
        'canonical_url': request.build_absolute_uri(request.path),
        'og_type': 'website',
    }
    
    context = {
        'category': {'slug': category_slug, 'name': category_label},
        'page_obj': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'seo': seo_data,
    }
    return render(request, 'blog/category.html', context)

def blog_tag(request, tag_slug):
    """Posts filtered by tag with SEO optimization"""
    tag = get_object_or_404(Tag, slug=tag_slug)
    
    # Get posts with this tag
    posts_list = BlogPost.objects.filter(
        tags=tag,
        status='published',
        published_date__lte=timezone.now()
    ).select_related().prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for sidebar
    categories = []
    for choice_value, choice_label in BlogPost.CATEGORY_CHOICES:
        count = BlogPost.objects.filter(
            status='published',
            published_date__lte=timezone.now(),
            category=choice_value
        ).count()
        if count > 0:
            categories.append({
                'name': choice_label,
                'slug': choice_value,
                'post_count': count
            })
    
    # Get popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count('blogpost')
    ).filter(post_count__gte=2).order_by('-post_count')[:10]
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).order_by('-published_date')[:5]
    
    # SEO Meta Data
    seo_data = {
        'title': f'Posts tagged "{tag.name}" - Dating Hub Research',
        'meta_description': f'Explore all articles tagged {tag.name} from Dating Hub Research Team. Expert insights on modern dating and relationships.',
        'meta_keywords': f'{tag.name}, dating advice, relationship tips, {tag.slug}',
        'canonical_url': request.build_absolute_uri(request.path),
        'og_type': 'website',
    }
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'seo': seo_data,
    }
    return render(request, 'blog/tag.html', context)
