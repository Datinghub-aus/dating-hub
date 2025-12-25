from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def format_blog_content(value):
    """
    Convert plain text to formatted HTML with paragraphs.
    """
    if not value:
        return ""
    
    # Clean the text
    text = value.strip()
    
    # Split by any sequence of 2 or more newlines
    parts = re.split(r'\n\s*\n+', text)
    
    result_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Check if it looks like a heading
        words = part.split()
        is_short = len(words) < 8
        ends_with_colon = part.endswith(':')
        starts_with_the = part.startswith('The ')
        starts_with_key = part.startswith('Key ')
        
        if (is_short and (ends_with_colon or starts_with_the or starts_with_key)):
            # It's a heading
            result_parts.append(f'<h3 class="content-heading">{part}</h3>')
        elif 'Key Finding:' in part or ('%' in part and ':' in part):
            # It's a key finding or statistic
            result_parts.append(f'<div class="key-finding">{part}</div>')
        else:
            # Regular paragraph - replace single newlines with <br>
            part = part.replace('\n', '<br>')
            result_parts.append(f'<p class="blog-paragraph">{part}</p>')
    
    # Join all parts and mark as safe
    result = ''.join(result_parts)
    return mark_safe(result)
