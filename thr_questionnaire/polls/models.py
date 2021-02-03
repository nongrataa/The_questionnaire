from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=50, blank=True)
    published = models.BooleanField(default=False, verbose_name='Опубликовать?')
    url_access = models.BooleanField(default=False, verbose_name='Доступ к опросу только по ссылке')

    def __str__(self):
        return self.question_text


class Chois(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    respondent = models.TextField(blank=True)

    def __str__(self):
        return self.choice_text
