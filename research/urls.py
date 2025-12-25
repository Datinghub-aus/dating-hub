# research/urls.py - SIMPLE WORKING VERSION
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Home page - NEW pretty landing page
    path('', views.home, name='home'),
    
    # About page
    path('about/', TemplateView.as_view(template_name='pages/about/index.html'), name='about'),
    
    # Research pages
    path('research/', views.research_index, name='research_index'),
    path('research/micromance/', views.micromance, name='micromance'),
    path('research/ai-matchmaking/', views.ai_matchmaking, name='ai_matchmaking'),
    path('research/digital-boundaries/', views.digital_boundaries, name='digital_boundaries'),
    path('research/methodology/', views.methodology, name='methodology'),
    path('research/ethics/', views.research_ethics, name='research_ethics'),
    
    # Tools pages
    path('tools/data-library/', views.data_library, name='data_library'),
    path('tools/privacy/', views.privacy, name='privacy'),
    path('tools/terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    
    # AI Dating Survey
    path('tools/dating-recommendations/', views.dating_recommendations_survey, name='dating_recommendations'),
    path('tools/thank-you/', views.thank_you_page, name='thank_you_page'),
]
