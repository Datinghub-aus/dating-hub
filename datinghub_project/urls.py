# datinghub_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('research.urls')),  # Include research app URLs
    path('blog/', include('blog.urls')),  # Include blog app URLs
    path('health/', health_check, name='health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
