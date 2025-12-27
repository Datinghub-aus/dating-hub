from django.db import models

class SurveySubmission(models.Model):
    """Stores all survey submissions for admin viewing"""
    # User Information
    name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="User Name"
    )
    email = models.EmailField(
        verbose_name="Email Address"
    )
    
    # Survey Details
    survey_type = models.CharField(
        max_length=50,
        choices=[
            ('completed', 'Completed Survey - Personalized Recommendations'),
            ('skipped', 'Skipped Survey - Basic Recommendations'),
        ],
        default='completed',
        verbose_name="Survey Type"
    )
    
    # Survey Answers (stored as JSON for flexibility)
    answers = models.JSONField(
        blank=True, 
        null=True,
        verbose_name="Survey Answers",
        help_text="JSON format of all survey questions and answers"
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Submission Time"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )
    
    # Admin Management
    processed = models.BooleanField(
        default=False,
        verbose_name="Processed",
        help_text="Mark as processed when recommendations have been sent"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Admin Notes",
        help_text="Internal notes about this submission"
    )
    
    def __str__(self):
        """String representation for admin panel"""
        if self.name:
            return f"{self.name} - {self.email}"
        return f"Anonymous - {self.email}"
    
    def get_answer_count(self):
        """Get number of questions answered"""
        if self.answers:
            return len(self.answers)
        return 0
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Survey Submission"
        verbose_name_plural = "Survey Submissions"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['submitted_at']),
            models.Index(fields=['processed']),
        ]
