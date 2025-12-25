# research/views.py - SIMPLIFIED
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# ===== HOME PAGE =====
def home(request):
    """New attractive standalone homepage"""
    return render(request, 'home/index.html')  # Your pretty page

# ===== RESEARCH PAGES =====
def research_index(request):
    return render(request, 'research/index.html')

def micromance(request):
    return render(request, 'research/micromance.html')

def ai_matchmaking(request):
    return render(request, 'research/ai-matchmaking.html')

def methodology(request):
    return render(request, 'research/methodology.html')

def research_ethics(request):
    return render(request, 'research/research-ethics.html')

def digital_boundaries(request):
    return render(request, 'research/digital-boundaries.html')

# ===== TOOLS/LEGAL PAGES =====
def data_library(request):
    return render(request, 'tools/data_library.html')

def privacy(request):
    return render(request, 'tools/privacy.html')

def terms(request):
    return render(request, 'tools/terms.html')

def contact(request):
    return render(request, 'tools/contact.html')

# ===== AI DATING RECOMMENDATIONS SURVEY =====
def dating_recommendations_survey(request):
    """AI Dating Site Matchmaker Survey - Just collects data"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        skip_survey = request.POST.get('skip_survey', '')
        
        # Validate email
        if not email or '@' not in email:
            messages.error(request, 'Please provide a valid email address.')
            return render(request, 'tools/dating_recommendations.html')
        
        # Prepare data for email
        if skip_survey:
            # User skipped survey
            survey_type = "Skipped Survey - Basic Recommendations"
            answers = None
        else:
            # User completed survey - UPDATED WITH GENDER FIELD
            survey_type = "Completed Survey - Personalized Recommendations"
            answers = {
                'gender': request.POST.get('gender', ''),
                'q1': request.POST.get('q1', ''),
                'q2': request.POST.get('q2', ''),
                'q3': request.POST.get('q3', ''),
                'q4': request.POST.get('q4', ''),
                'q5': request.POST.get('q5', ''),
                'q6': request.POST.get('q6', '')
            }
        
        # Send confirmation email
        send_confirmation_email(email, name, survey_type, answers)
        
        messages.success(request, 'Your dating site recommendations will arrive within 72 hours! Check your email.')
        return redirect('thank_you_page')
    
    return render(request, 'tools/dating_recommendations.html')

def thank_you_page(request):
    """Thank you page after survey submission"""
    return render(request, 'tools/thank_you.html')

def send_confirmation_email(email, name, survey_type, answers):
    """Send confirmation email - YOU WILL REPLACE THIS LATER"""
    subject = "Dating Site Recommendations - Coming Soon!"
    
    # Basic email for now - you'll replace with proper template later
    message = f"""Hi {name if name else 'there'},

Thank you for using our AI Dating Site Matchmaker!

We've received your request for dating site recommendations.

{survey_type}

Our team will analyze your preferences and send personalized recommendations within 72 hours.

In the meantime, you can browse our research:
https://dating-hub.com.au/research/

Best regards,
Dating Hub Research Team
"""
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    
    # OPTIONAL: Also send to yourself to know someone signed up
    admin_message = f"""New Dating Recommendations Request:

Email: {email}
Name: {name if name else 'Not provided'}
Type: {survey_type}

Answers: {answers if answers else 'Survey skipped'}

Send recommendations within 72 hours.
"""
    
    send_mail(
        "New Dating Recommendations Request",
        admin_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],  # Send to yourself
        fail_silently=False,
    )
