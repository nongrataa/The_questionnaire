from django.shortcuts import render, get_object_or_404, loader, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import *
from .forms import *
from django.forms import inlineformset_factory

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

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.chois_set.get(pk=request.POST['choice'])
    except (KeyError, Chois.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('result', args=(question.id,)))


def add_question(request):

    if request.method == 'POST':
        question = Question.objects.all()

        form_question = AddQuestionForm(request.POST)
        form_chois = ChoisForm(request.POST)

        if form_question.is_valid() and form_chois.is_valid():

            form_question.save()
            form_chois.save()
            return redirect('index')

        else:
            context = {
                'form_question': form_question,
                'form_chois': form_chois,
                'question': question,
            }

    else:
        context = {
            'form_question': AddQuestionForm(),
            'form_chois': ChoisForm(),
        }
    return render(request, 'polls/add_question.html', context)