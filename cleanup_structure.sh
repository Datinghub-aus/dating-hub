#!/bin/bash

echo "=== DATINGHUB 2026 STRUCTURE CLEANUP ==="
echo "This will reorganize your project into a clean Django structure."
echo ""

# 1. Stop any running servers
echo "1. Stopping any running Django servers..."
pkill -f "runserver" 2>/dev/null || true
sleep 2

# 2. Backup everything
echo "2. Creating backups..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r templates "$BACKUP_DIR/" 2>/dev/null || true
cp datinghub/urls.py "$BACKUP_DIR/" 2>/dev/null || true
cp datinghub/settings.py "$BACKUP_DIR/" 2>/dev/null || true
echo "   Backup created in: $BACKUP_DIR"

# 3. Check current structure
echo "3. Checking current structure..."
if [ ! -d "datinghub" ]; then
    echo "   ERROR: datinghub/ folder not found!"
    exit 1
fi

# 4. Move project folder to proper name
echo "4. Renaming project folder..."
if [ -d "datinghub" ]; then
    mv datinghub datinghub_project
    echo "   Renamed: datinghub/ -> datinghub_project/"
fi

# 5. Create proper project structure
echo "5. Creating proper structure..."
mkdir -p datinghub_2026_project
if [ -d "datinghub_project" ]; then
    mv datinghub_project/* datinghub_2026_project/ 2>/dev/null || true
    rmdir datinghub_project 2>/dev/null || true
fi

# 6. Update manage.py
echo "6. Updating manage.py..."
if [ -f "manage.py" ]; then
    sed -i '' "s/datinghub.settings/datinghub_2026_project.settings/" manage.py
    echo "   Updated settings module in manage.py"
fi

# 7. Fix BASE_DIR in settings
echo "7. Fixing BASE_DIR in settings..."
if [ -f "datinghub_2026_project/settings.py" ]; then
    sed -i '' "s/BASE_DIR = Path(__file__).resolve().parent.parent/BASE_DIR = Path(__file__).resolve().parent.parent.parent/" datinghub_2026_project/settings.py
    echo "   Fixed BASE_DIR path"
fi

# 8. Create main research_hub app
echo "8. Creating research_hub app..."
python3 manage.py startapp research_hub 2>/dev/null || echo "   research_hub already exists or error"

# 9. Organize templates into research_hub
echo "9. Organizing templates..."
mkdir -p research_hub/templates/research_hub 2>/dev/null

if [ -d "templates/home" ]; then
    mv templates/home research_hub/templates/research_hub/ 2>/dev/null || true
    echo "   Moved: templates/home/ -> research_hub/templates/research_hub/"
fi

if [ -d "templates/blog" ]; then
    mv templates/blog research_hub/templates/research_hub/ 2>/dev/null || true
    echo "   Moved: templates/blog/ -> research_hub/templates/research_hub/"
fi

if [ -d "templates/tools" ]; then
    mv templates/tools research_hub/templates/research_hub/ 2>/dev/null || true
    echo "   Moved: templates/tools/ -> research_hub/templates/research_hub/"
fi

if [ -d "templates/directory" ]; then
    mv templates/directory research_hub/templates/research_hub/ 2>/dev/null || true
    echo "   Moved: templates/directory/ -> research_hub/templates/research_hub/"
fi

# 10. Remove empty templates dir
rmdir templates 2>/dev/null || true

# 11. Remove duplicate settings from api/
echo "10. Cleaning up duplicate files..."
rm -f api/settings.py 2>/dev/null || true
echo "   Removed: api/settings.py"

# 12. Create research_hub views
echo "11. Creating research_hub views..."
cat > research_hub/views.py << 'VIEWS_EOF'
from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'research_hub/home/index.html'

class BlogIndexView(TemplateView):
    template_name = 'research_hub/blog/index.html'

class MicromanceView(TemplateView):
    template_name = 'research_hub/blog/micromance.html'

class AIMatchmakingView(TemplateView):
    template_name = 'research_hub/blog/ai_matchmaking.html'

class DigitalBoundariesView(TemplateView):
    template_name = 'research_hub/blog/digital_boundaries.html'

class DataLibraryView(TemplateView):
    template_name = 'research_hub/tools/data_library.html'

class PrivacyView(TemplateView):
    template_name = 'research_hub/tools/privacy.html'

class TermsView(TemplateView):
    template_name = 'research_hub/tools/terms.html'

class DirectoryView(TemplateView):
    template_name = 'research_hub/directory/index.html'
VIEWS_EOF
echo "   Created research_hub/views.py"

# 13. Create research_hub URLs
echo "12. Creating research_hub URLs..."
cat > research_hub/urls.py << 'URLS_EOF'
from django.urls import path
from . import views

app_name = 'research_hub'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogIndexView.as_view(), name='blog_index'),
    path('blog/micromance/', views.MicromanceView.as_view(), name='micromance'),
    path('blog/ai-matchmaking/', views.AIMatchmakingView.as_view(), name='ai_matchmaking'),
    path('blog/digital-boundaries/', views.DigitalBoundariesView.as_view(), name='digital_boundaries'),
    path('tools/data-library/', views.DataLibraryView.as_view(), name='data_library'),
    path('tools/privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('tools/terms/', views.TermsView.as_view(), name='terms'),
    path('directory/', views.DirectoryView.as_view(), name='directory'),
]
URLS_EOF
echo "   Created research_hub/urls.py"

# 14. Create main project URLs
echo "13. Creating main project URLs..."
cat > datinghub_2026_project/urls.py << 'MAIN_URLS_EOF'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('research_hub.urls')),
    path('articles/', include('blog.urls')),
    path('leads/', include('leads.urls')),
    path('api/', include('api.urls')),
    path('old/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
MAIN_URLS_EOF
echo "   Created datinghub_2026_project/urls.py"

# 15. Update INSTALLED_APPS
echo "14. Updating INSTALLED_APPS..."
if [ -f "datinghub_2026_project/settings.py" ]; then
    # Create a clean INSTALLED_APPS section
    sed -i '' "/INSTALLED_APPS = \[/,/\]/c\\
INSTALLED_APPS = [\\
    'django.contrib.admin',\\
    'django.contrib.auth',\\
    'django.contrib.contenttypes',\\
    'django.contrib.sessions',\\
    'django.contrib.messages',\\
    'django.contrib.staticfiles',\\
    'research_hub',\\
    'blog',\\
    'leads',\\
    'api',\\
    'core',\\
]" datinghub_2026_project/settings.py
    echo "   Updated INSTALLED_APPS"
fi

echo ""
echo "=== CLEANUP COMPLETE! ==="
echo ""
echo "New structure:"
echo "  datinghub_2026_project/    - Django project (settings, main URLs)"
echo "  research_hub/              - Main app for Dating Hub Research"
echo "  blog/, leads/, api/, core/ - Original apps"
echo ""
echo "To test:"
echo "  1. cd /Users/carlsng/datinghub_2026"
echo "  2. python3 manage.py runserver"
echo "  3. Visit: http://localhost:8000/"
echo ""
echo "Backup saved in: $BACKUP_DIR"
