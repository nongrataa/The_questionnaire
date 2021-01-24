
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:question_id>/', detail, name='detail'),
    path('<int:question_id>/result/', result, name='result'),
    path('<int:question_id>/vote/', vote, name='vote'),
]
