# models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('psychology', 'Psychology & Behavior'),
        ('technology', 'Technology & Algorithms'),
        ('sociology', 'Sociology & Trends'),
        ('data', 'Data Analysis'),
        ('ethics', 'Ethics & Policy'),
        ('culture', 'Culture & Society'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author_initials = models.CharField(max_length=10, default='DHR')
    content = models.TextField()
    excerpt = models.TextField(max_length=500, help_text="Brief summary for listings")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Publication info
    published_date = models.DateField(default=timezone.now)
    read_time = models.IntegerField(help_text="Estimated read time in minutes", default=5)
    
    # Status
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
