
from django.contrib import admin
from django.urls import path
from .views import *

# urlpatterns = [
#     path('', index, name='index'),
#     path('<int:question_id>/', detail, name='detail'),
#     path('<int:question_id>/result/', result, name='result'),
#     path('<int:question_id>/vote/', vote, name='vote'),
# ]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add_question/', add_question, name='add_question'),
    path('add_choice/<int:pk>/', add_choice, name='add_choice'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('<int:pk>/result/', ResultsView.as_view(), name='result'),
    path('<int:question_id>/vote/', vote, name='vote'),
]
