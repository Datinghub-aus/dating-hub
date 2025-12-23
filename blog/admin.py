# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_initials', 'category', 'published_date', 'status', 'views_display')
    list_filter = ('status', 'category', 'published_date')
    search_fields = ('title', 'content', 'excerpt', 'author_initials')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author_initials', 'excerpt', 'category')
        }),
        ('Content', {
            'fields': ('content', 'featured_image')
        }),
        ('Publication', {
            'fields': ('published_date', 'read_time', 'status')
        }),
    )
    
    def views_display(self, obj):
        return f"{obj.views} views"
    views_display.short_description = 'Views'
    
    # Add a custom action for bulk publishing
    actions = ['make_published']
    
    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected posts as published"
