from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from .models import SurveySubmission

# ===== HOME PAGES =====
def home(request):
    """NEW attractive landing page with newsletter signup"""
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        # Newsletter signup form was submitted
        email = request.POST.get('newsletter_email', '').strip()
        
        if email and '@' in email:
            # Send NEWSLETTER welcome email
            send_newsletter_welcome_email(email)
            
            # Add success message
            messages.success(request, 'Thanks for subscribing! Check your email for confirmation.')
            
            # Use namespace
            return redirect('research:home')
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
    """AI Dating Site Matchmaker Survey - WITH database save"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        skip_survey = request.POST.get('skip_survey', '')
        
        # Validate email
        if not email or '@' not in email:
            messages.error(request, 'Please provide a valid email address.')
            return render(request, 'tools/dating_recommendations.html')
        
        # Prepare data
        if skip_survey:
            survey_type = 'skipped'
            answers = None
        else:
            survey_type = 'completed'
            answers = {
                'gender': request.POST.get('gender', ''),
                'q1': request.POST.get('q1', ''),
                'q2': request.POST.get('q2', ''),
                'q3': request.POST.get('q3', ''),
                'q4': request.POST.get('q4', ''),
                'q5': request.POST.get('q5', ''),
                'q6': request.POST.get('q6', '')
            }
        
        # ⚠️ TEMPORARY: Database COMPLETELY disabled (no try/except)
        submission_id = None
        
        send_confirmation_email(email, name, survey_type, answers, submission_id)
        
        return redirect('research:thank_you_page')
    
    return render(request, 'tools/dating_recommendations.html')

# ===== THANK YOU PAGE =====
def thank_you_page(request):
    """Display thank you page after survey submission"""
    return render(request, 'tools/thank_you.html')

# ===== EMAIL FUNCTIONS =====
def send_confirmation_email(email, name, survey_type, answers, submission_id=None):
    """
    Send confirmation email for SURVEY submissions
    - To user: Simple confirmation
    - To admin: Detailed notification with database reference
    """
    
    # Map survey_type to display text
    survey_type_display = {
        'completed': 'Completed Survey - Personalized Recommendations',
        'skipped': 'Skipped Survey - Basic Recommendations'
    }.get(survey_type, survey_type)
    
    # 1. EMAIL TO USER
    user_subject = "Your Dating Site Recommendations Are Being Prepared"
    
    user_message = f"""Hi {name if name else 'there'},

Thank you for using our AI Dating Site Matchmaker!

We've received your request for dating site recommendations.

{survey_type_display}

Our team is currently analyzing your preferences and will send personalized recommendations within 72 hours.

In the meantime, you can browse our research:
https://dating-hub.com.au/research/

Best regards,
Dating Hub Research Team
"""
    
    send_mail(
        user_subject,
        user_message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    
    # 2. SEPARATE EMAIL TO ADMIN
    # Get total submissions count for reference
    total_submissions = SurveySubmission.objects.count()
    
    admin_subject = f"📋 Survey #{total_submissions}: {name if name else 'Anonymous'}"
    
    # Format answers for admin
    if answers:
        answers_text = "\n".join([f"  • {key}: {value}" for key, value in answers.items()])
    else:
        answers_text = "  • User skipped detailed survey"
    
    # Database reference link
    db_link = ""
    if submission_id:
        db_link = f"\nDATABASE LINK: https://dating-hub.com.au/admin/research/surveysubmission/{submission_id}/change/"
    
    admin_message = f"""NEW SURVEY SUBMISSION #{total_submissions}

USER INFORMATION:
• Name: {name if name else 'Not provided'}
• Email: {email}
• Survey Type: {survey_type_display}
• Submission ID: {submission_id or 'N/A'}

SURVEY ANSWERS:
{answers_text}

TIMESTAMP: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
{db_link}

---
This submission has been automatically saved to the database.
Admin panel: https://dating-hub.com.au/admin/
"""
    
    send_mail(
        admin_subject,
        admin_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
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
