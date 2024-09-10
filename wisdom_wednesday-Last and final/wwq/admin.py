from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from .models import Quote, Blog, DepartmentPage, UserDetail, QuizQuestion, QuizResult
from import_export import resources, fields
from import_export.widgets import DateTimeWidget
from import_export.admin import ExportMixin

# Define a resource for QuizResult
class QuizResultResource(resources.ModelResource):
    # Explicitly define the date_taken field with a DateTime widget to ensure proper formatting
    date_taken = fields.Field(column_name='date_taken', attribute='date_taken', widget=DateTimeWidget(format='%Y-%m-%d %H:%M:%S'))

    class Meta:
        model = QuizResult
        fields = ('user__name', 'user__employee_id', 'user__department', 'score', 'date_taken')  # Include 'date_taken' in the export

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': AdminDateWidget},  # Use the correct AdminDateWidget
    }
    list_display = ('title', 'volume', 'part', 'published_date', 'author')  # Include 'volume', 'part', and 'author' in display
    ordering = ('volume', 'part')  # Order by 'volume' and 'part'
    fields = ('title', 'volume', 'part', 'content', 'additional_content', 'published_date', 'week', 'image', 'additional_image', 'author', 'author_photo')  # Manage multiple content and image fields

@admin.register(DepartmentPage)
class DepartmentPageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'department', 'submission_date')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'correct_option')
    list_filter = ('correct_option',)

@admin.register(QuizResult)
class QuizResultAdmin(ExportMixin, admin.ModelAdmin):  # ExportMixin to add export functionality
    resource_class = QuizResultResource
    list_display = ('user', 'score', 'date_taken', 'get_department')  # Use the custom method
    list_filter = ('date_taken', 'score', 'user__department')  # Filtering by 'date_taken', 'score', and 'department'

    def get_department(self, obj):
        return obj.user.department  # Assuming the 'department' is a field on the User model
    get_department.short_description = 'Department'  # Optional: Customize column name
