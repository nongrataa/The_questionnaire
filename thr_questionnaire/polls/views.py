from django.shortcuts import render, get_object_or_404, loader, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.base import View
from transliterate import translit, get_available_language_codes
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.

#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question
#     }
#     return render(request, 'polls/detail.html', context)
#
#
# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/result.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    #Выводим только те вопросы на которые не отвечали
    def get_queryset(self):
        user = self.request.user.id
        question = Question.objects.all()
        resp_list = []
        for resp in question:
            if str(user) not in resp.respondent.split(' '):
                resp_list.append(resp.id)
        return Question.objects.filter(pk__in=resp_list)


class IndexView2(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Chois.objects.order_by('question')

#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#     def get_queryset(self):
#         return Question.objects.filter(pk=self.kwargs['pk'])
#
#     def get_question(self):
#         user = self.request.user.id
#         choise = Chois.objects.filter(question=self.kwargs['pk'])
#         resp_list = []
#         for resp in choise:
#             for i in resp.respondent.split(' '):
#                 resp_list.append(i)
#         if str(user) in resp_list:
#             return redirect('result', self.get_queryset.id)
#         else:
#             context = {
#                 'question': self.get_queryset()
#             }
#             return render(self.request, 'polls/detail.html', context)


def detail(request, pk):
    user = request.user.id
    choise = Chois.objects.filter(question=pk)
    resp_list = []
    for resp in choise:
        for i in resp.respondent.split(' '):
            resp_list.append(i)
    if str(user) in resp_list:
        return redirect('result', pk)
    else:
        question = get_object_or_404(Question, pk=pk)
        context = {
            'question': question
        }
        return render(request, 'polls/detail.html', context)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

# Тут возможно стоит переделать
def vote(request, question_id):
    print('request.user.id', request.user.id)
    if request.user.id == None:
        return redirect('register')
    else:
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.chois_set.get(pk=request.POST['choice'])
            selected_question = question
            print('select_choise', selected_choice)
        except (KeyError, Chois.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            user = request.user.id
            choise = Chois.objects.filter(question=question_id)
            resp_list = []
            for resp in choise:
                for i in resp.respondent.split(' '):
                    resp_list.append(i)
            if str(user) in resp_list:
                print('True')
                return HttpResponse("Вы уже голосовали")
            else:
                selected_choice.votes += 1
                selected_choice.respondent += ' ' + str(request.user.id)
                selected_question.respondent += ' ' + str(request.user.id)
                selected_choice.save()
                selected_question.save()
                return HttpResponseRedirect(reverse('result', args=(question.id,)))


def add_question(request):
    if request.method == 'POST':
        question = Question.objects.all()
        form_question = AddQuestionForm(request.POST)
        if form_question.is_valid():
            # тут мы меняем поле формы URL что бы в каждом вопросе оно менялось,
            # возможно стоит написать функцию для транслитерации текста
            new_form = form_question.save(commit=False)
            url = form_question.cleaned_data['url']
            new_form.url = str(request.user.id) + str(len(question))
            new_form.save()
            return redirect('add_choice', pk=new_form.id)
        else:
            context = {
                'form_question': form_question,
                'question': question,
            }
    else:
        context = {
            'form_question': AddQuestionForm(),
        }
    return render(request, 'polls/add_question.html', context)


def add_choice(request, pk):
    button = request.POST.get('save_add')
    if button == '':
        question = Question.objects.get(pk=pk)
        ChoiceFormset = inlineformset_factory(Question, Chois, fields=('choice_text',))
        if request.method == 'POST':
            formset = ChoiceFormset(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('add_choice', pk=question.id)
    else:
        question = Question.objects.get(pk=pk)
        ChoiceFormset = inlineformset_factory(Question, Chois, fields=('choice_text',))
        if request.method == 'POST':
            formset = ChoiceFormset(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('index')
    formset = ChoiceFormset(instance=question)
    context = {
        'formset': formset
    }
    return render(request, 'polls/add_choice.html', context)


def my_questions(request):
    user = request.user.id
    question = Question.objects.filter(author=user)
    context = {
        "my_questions": question
    }
    return render(request, 'polls/myquestions.html', context)


def user_questions(request, userid):
    question = Question.objects.filter(author=userid, url_access=False)
    author = User.objects.get(pk=userid)
    print('author - ', author)
    context = {
        "user_questions": question,
        "author": author,
    }
    return render(request, 'polls/user_questions.html', context)


def register(request):
    if request.method == "POST":
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            messages.success(request, 'Вы успешно зарегистировались')
            login(request, user)
            return redirect('index')
    else:
        register_form = UserRegisterForm()
    context = {
        'form': register_form
    }
    return render(request, 'polls/register.html', context)


def user_login(request):
    if request.method == "POST":
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('index')
    else:
        login_form = UserLoginForm()
    context = {
        "login_form": login_form,
    }
    return render(request, 'polls/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')