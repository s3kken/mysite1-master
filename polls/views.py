from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from .forms import Registration
from .models import Question, Choice, Vote, User
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/home_page.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        question.question_votes += 1
        question.question_votes.save()
        user_choice = Vote.objects.create(question=question, user=request.user)
        user_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class RegisterUser(CreateView):
    form_class = Registration
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_page = 'registration'


class PersonalAccount(generic.ListView):
    model = User
    template_name = 'polls/personal_account.html'


class UpdateDate(generic.UpdateView):
    model = User
    template_name = 'polls/update_account.html'
    success_url = '/'
    fields = ('username', 'avatar')

    def get_object(self, queryset=None):
        objs = super(UpdateDate, self).get_object(queryset)
        if objs != self.request.user:
            raise PermissionDenied()
        else:
            return self.request.user
