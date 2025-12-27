from django.contrib import admin
from django.utils.html import format_html
from .models import SurveySubmission

@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    # ===== LIST VIEW CONFIGURATION =====
    list_display = [
        'email_display', 
        'name_display', 
        'survey_type_display',
        'answer_count',
        'submitted_at_display',
        'processed',  # Direct field for editing
        'view_details_link'
    ]
    
    list_filter = [
        'survey_type',
        'processed',
        'submitted_at',
    ]
    
    search_fields = [
        'name',
        'email',
        'notes',
    ]
    
    list_editable = ['processed']
    
    list_per_page = 25
    
    actions = [
        'mark_as_processed',
        'mark_as_unprocessed',
    ]
    
    # ===== DETAIL VIEW CONFIGURATION =====
    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'survey_type'),
            'classes': ('wide',),
        }),
        ('Survey Data', {
            'fields': ('answers_display',),
            'classes': ('collapse', 'wide'),
            'description': 'All submitted answers in readable format'
        }),
        ('Admin Management', {
            'fields': ('processed', 'notes', 'submitted_at', 'updated_at'),
            'classes': ('wide',),
        }),
    )
    
    readonly_fields = [
        'submitted_at', 
        'updated_at',
        'answers_display'
    ]
    
    # ===== CUSTOM METHODS =====
    def email_display(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_display.short_description = 'Email'
    
    def name_display(self, obj):
        return obj.name if obj.name else 'Anonymous'
    name_display.short_description = 'Name'
    
    def survey_type_display(self, obj):
        if obj.survey_type == 'completed':
            return format_html('<span style="color: green;">✓ Completed</span>')
        return format_html('<span style="color: orange;">⏭ Skipped</span>')
    survey_type_display.short_description = 'Type'
    
    def answer_count(self, obj):
        count = 0
        if obj.answers:
            count = len(obj.answers)
        color = 'green' if count > 0 else 'gray'
        text = f"{count} answers" if count > 0 else "Skipped"
        return format_html('<span style="color: {};">{}</span>', color, text)
    answer_count.short_description = 'Answers'
    
    def submitted_at_display(self, obj):
        return obj.submitted_at.strftime('%Y-%m-%d %H:%M')
    submitted_at_display.short_description = 'Submitted'
    
    def view_details_link(self, obj):
        url = f"/admin/research/surveysubmission/{obj.id}/change/"
        return format_html(
            '<a href="{}" style="background: #4CAF50; color: white; padding: 2px 8px; border-radius: 3px;">View</a>',
            url
        )
    view_details_link.short_description = 'Actions'
    
    def answers_display(self, obj):
        if not obj.answers:
            return "User skipped the detailed survey"
        
        html = '<div style="background: #f5f5f5; padding: 10px; border-radius: 5px;">'
        for key, value in obj.answers.items():
            html += f'<div><strong>{key}:</strong> {value}</div>'
        html += '</div>'
        return format_html(html)
    answers_display.short_description = 'Answers'
    
    # ===== ADMIN ACTIONS =====
    def mark_as_processed(self, request, queryset):
        updated = queryset.update(processed=True)
        self.message_user(request, f"Marked {updated} submissions as processed.")
    mark_as_processed.short_description = "Mark as processed"
    
    def mark_as_unprocessed(self, request, queryset):
        updated = queryset.update(processed=False)
        self.message_user(request, f"Marked {updated} submissions as unprocessed.")
    mark_as_unprocessed.short_description = "Mark as unprocessed"
