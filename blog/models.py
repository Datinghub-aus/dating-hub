# blog/models.py - UPDATED VERSION with SEO optimizations
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=60)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['name']

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('research', 'Research Insights'),
        ('trends', 'Dating Trends'),
        ('technology', 'Technology & Dating'),
        ('psychology', 'Relationship Psychology'),
        ('advice', 'Practical Advice'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    # SEO-optimized fields
    title = models.CharField(max_length=200, help_text="Keep under 60 characters for optimal SEO")
    slug = models.SlugField(unique=True, max_length=200, help_text="Auto-generated from title")
    excerpt = models.TextField(max_length=500, blank=True, help_text="Meta description - keep under 160 characters")
    content = models.TextField(help_text="Use proper HTML headings (h2, h3) for SEO")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='research')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # SEO-optimized image fields
    featured_image = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, null=True, 
                                      help_text="Recommended size: 1200x630px for social sharing")
    featured_image_alt = models.CharField(max_length=200, blank=True, 
                                         help_text="Alt text for SEO and accessibility")
    
    # Author information
    author = models.CharField(max_length=100, default='Dating Hub Research Team')
    author_bio = models.TextField(blank=True, max_length=300, 
                                 default='Dating Hub Research Team provides insights into modern dating trends, relationship psychology, and data-driven advice for successful connections.')
    
    # SEO-optimized meta fields
    meta_title = models.CharField(max_length=200, blank=True, 
                                 help_text="Custom meta title (optional). Leave blank to use post title.")
    meta_description = models.TextField(max_length=300, blank=True, 
                                       help_text="Custom meta description (optional). Leave blank to use excerpt.")
    
    # Content organization
    tags = models.ManyToManyField(Tag, blank=True)
    read_time = models.PositiveIntegerField(default=5, 
                                           help_text="Estimated reading time in minutes (calculated at 200 words/min)")
    
    # Dates and tracking
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    # Engagement metrics
    views = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    
    # SEO structure
    is_featured = models.BooleanField(default=False)
    canonical_url = models.URLField(blank=True, help_text="Canonical URL for SEO (if republished)")
    
    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['slug', 'status']),
            models.Index(fields=['published_date', 'status']),
            models.Index(fields=['category', 'status']),
        ]
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if empty
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate meta fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:200]
        
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:300]
        elif not self.meta_description:
            # Generate from content
            content_preview = self.content[:297] + '...' if len(self.content) > 300 else self.content
            self.meta_description = content_preview
        
        # Calculate read_time from word count (assuming 200 words per minute)
        word_count = len(self.content.split())
        self.read_time = max(1, word_count // 200)
        
        super().save(*args, **kwargs)
    
    def get_author_initials(self):
        """Return DHR for Dating Hub Research"""
        return 'DHR'
    
    def get_category_display_name(self):
        """Get full category name"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_keywords(self):
        """Generate keywords for meta tags"""
        keywords = [self.category]
        keywords.extend([tag.name for tag in self.tags.all()])
        return ', '.join(keywords)
    
    @property
    def word_count(self):
        """Calculate word count for SEO"""
        return len(self.content.split())
