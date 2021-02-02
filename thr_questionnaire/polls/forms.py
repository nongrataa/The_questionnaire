from django import forms
from .models import *


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'author', 'url', 'published', 'url_access']
