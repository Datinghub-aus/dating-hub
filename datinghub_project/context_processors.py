from django.conf import settings

def site_settings(request):
    """Add site settings to template context."""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Dating Hub'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', ''),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
        'DEBUG': settings.DEBUG,
    }
