from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# ===== HOME PAGES =====
def home(request):
    """NEW attractive landing page with newsletter signup"""
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        # Newsletter signup form was submitted
        email = request.POST.get('newsletter_email', '').strip()
        
        if email and '@' in email:
            # Send NEWSLETTER welcome email (different from survey email)
            send_newsletter_welcome_email(email)
            
            # Add success message
            messages.success(request, 'Thanks for subscribing! Check your email for confirmation.')
            
            # Redirect to avoid form resubmission on refresh
            return redirect('home')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return render(request, 'home/index.html')

# ===== RESEARCH PAGES =====
def research_index(request):
    return render(request, 'research/index.html')

def micromance(request):
    return render(request, 'research/micromance.html')

def ai_matchmaking(request):
    return render(request, 'research/ai_matchmaking.html')

def methodology(request):
    return render(request, 'research/methodology.html')

def research_ethics(request):
    return render(request, 'research/research_ethics.html')

def digital_boundaries(request):
    return render(request, 'research/digital_boundaries.html')

# ===== TOOLS/LEGAL PAGES =====
def data_library(request):
    return render(request, 'tools/data_library.html')

def privacy(request):
    return render(request, 'tools/privacy.html')

def terms(request):
    return render(request, 'tools/terms.html')

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
            # User completed survey
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
        
        # Send SURVEY confirmation email
        send_confirmation_email(email, name, survey_type, answers)
        
        # Redirect to the thank you page for SURVEY submissions
        return redirect('thank_you_page')
    
    return render(request, 'tools/dating_recommendations.html')

def thank_you_page(request):
    """Thank you page after SURVEY submission"""
    return render(request, 'research/thank_you.html')

# ===== EMAIL FUNCTIONS =====
def send_confirmation_email(email, name, survey_type, answers):
    """Send confirmation email for SURVEY submissions"""
    subject = "Your Dating Site Recommendations Are Being Prepared"
    
    message = f"""Hi {name if name else 'there'},

Thank you for using our AI Dating Site Matchmaker!

We've received your request for dating site recommendations.

{survey_type}

Our team is currently analyzing your preferences and will send personalized recommendations within 72 hours.

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

def send_newsletter_welcome_email(email):
    """Send welcome email for NEWSLETTER signups (from homepage)"""
    subject = "Welcome to Dating Hub's 2026 Dating Predictions!"
    
    message = f"""Welcome to Dating Hub's exclusive newsletter!

Thank you for subscribing to "Don't Just Date. Strategize."

You'll now receive:
• 2026 dating trend predictions
• Behavioral research insights
• Platform algorithm updates
• Success stories and case studies

Our first newsletter will arrive in your inbox soon.

In the meantime, explore our latest research:
https://dating-hub.com.au/research/

You can also try our AI Dating Site Matchmaker to get personalized platform recommendations:
https://dating-hub.com.au/tools/dating-recommendations/

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
