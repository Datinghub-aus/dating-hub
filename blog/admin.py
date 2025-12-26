# admin.py - SEO OPTIMIZED VERSION
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import BlogPost, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.blogpost_set.count()
    post_count.short_description = 'Posts'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # Display fields
    list_display = ('title', 'get_author_initials', 'category', 'status', 
                    'published_date', 'views_display', 'read_time_display', 
                    'seo_score')
    list_filter = ('status', 'category', 'published_date', 'is_featured', 'tags')
    search_fields = ('title', 'excerpt', 'content', 'author', 'tags__name')
    
    # Auto-slug generation
    prepopulated_fields = {'slug': ('title',)}
    
    # Date navigation
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    
    # Fieldsets for better organization
    fieldsets = (
        ('SEO Optimization', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'is_featured'),
            'classes': ('collapse',),
            'description': 'Optimize for search engines'
        }),
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'author_bio', 'excerpt', 'category')
        }),
        ('Content', {
            'fields': ('content', 'featured_image', 'featured_image_alt', 'tags')
        }),
        ('Publication & Metrics', {
            'fields': ('published_date', 'read_time', 'status', 'views', 'shares')
        }),
    )
    
    # Custom methods for display
    def get_author_initials(self, obj):
        """Return DHR for Dating Hub Research"""
        return 'DHR'
    get_author_initials.short_description = 'Author'
    
    def views_display(self, obj):
        return f"{obj.views:,} views"
    views_display.short_description = 'Views'
    views_display.admin_order_field = 'views'
    
    def read_time_display(self, obj):
        return f"{obj.read_time} min"
    read_time_display.short_description = 'Read Time'
    read_time_display.admin_order_field = 'read_time'
    
    def seo_score(self, obj):
        """Calculate a simple SEO score"""
        score = 0
        
        # Title length check (optimal: 50-60 chars)
        if 50 <= len(obj.title) <= 60:
            score += 25
        
        # Meta description check (optimal: 120-160 chars)
        if 120 <= len(obj.meta_description or obj.excerpt or '') <= 160:
            score += 25
        
        # Image alt text check
        if obj.featured_image_alt:
            score += 25
        
        # Content length check (optimal: 1000+ words)
        word_count = len(obj.content.split())
        if word_count >= 1000:
            score += 25
        
        # Color coding based on score
        if score >= 75:
            color = 'green'
        elif score >= 50:
            color = 'orange'
        else:
            color = 'red'
        
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{score}%</span>')
    seo_score.short_description = 'SEO Score'
    
    # Add custom actions
    actions = ['make_published', 'make_featured', 'update_read_time']
    
    def make_published(self, request, queryset):
        """Mark selected posts as published"""
        updated = queryset.update(status='published')
        self.message_user(request, f"{updated} posts published successfully.")
    make_published.short_description = "Mark selected posts as published"
    
    def make_featured(self, request, queryset):
        """Mark selected posts as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} posts marked as featured.")
    make_featured.short_description = "Mark selected posts as featured"
    
    def update_read_time(self, request, queryset):
        """Recalculate read time for selected posts"""
        for post in queryset:
            word_count = len(post.content.split())
            post.read_time = max(1, word_count // 200)
            post.save()
        self.message_user(request, f"Read time updated for {queryset.count()} posts.")
    update_read_time.short_description = "Recalculate read time"
    
    # Custom list filters
    list_filter = ('status', 'category', 'published_date', 'is_featured', 'tags')
    
    # Filters by date
    date_hierarchy = 'published_date'
    
    # Custom change form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Add help text to form fields
        form.base_fields['meta_title'].help_text = "Optimal: 50-60 characters"
        form.base_fields['meta_description'].help_text = "Optimal: 120-160 characters"
        form.base_fields['excerpt'].help_text = "Displayed on blog listing - optimal: 120-160 characters"
        
        return form
