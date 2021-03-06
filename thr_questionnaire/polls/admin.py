from django.contrib import admin
from .models import *

# Register your models here.


class ChoisInline(admin.TabularInline):
    model = Chois
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    list_display = ('question_text', 'pub_date')
    prepopulated_fields = {"url": ("question_text",)}
    fieldsets = [
        (None, {'fields': ['question_text', 'published', 'url_access']}),
        ('Information', {'fields': ['author', 'url', 'respondent']}),
    ]
    inlines = [ChoisInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Chois)

