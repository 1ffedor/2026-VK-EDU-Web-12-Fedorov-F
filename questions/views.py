from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import urlencode

from .forms import AnswerForm, AskQuestionForm
from .models import Answer, Question, Tag
from .utils import paginate


def _render_list(request, queryset, page_title, list_tab, tag_slug=''):
    page = paginate(queryset, request)
    return render(request, 'questions/list.html', {'page': page, 'page_title': page_title, 'list_tab': list_tab, 'tag': tag_slug})


def index(request):
    return _render_list(request, Question.objects.new(), 'Все вопросы', 'new')


def hot(request):
    return _render_list(request, Question.objects.hot(), 'Горячее', 'hot')


def tag(request, tag):
    tag_obj = get_object_or_404(Tag, slug=tag)
    return _render_list(
        request,
        Question.objects.by_tag(tag),
        tag_obj.name,
        'tag',
        tag_obj.name,
    )


def question_detail(request, pk):
    question = get_object_or_404(Question.objects.with_related(), pk=pk)
    answer_form = AnswerForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            login_url = f"{reverse('login')}?{urlencode({'next': request.get_full_path()})}"
            return redirect(login_url)
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(author=request.user, question=question)
            answer_pos = Answer.objects.filter(question=question).filter(
                Q(created_at__lt=answer.created_at) | Q(created_at=answer.created_at, pk__lte=answer.pk)
            ).count()
            answer_page = ((answer_pos - 1) // 10) + 1
            question_url = reverse('question_detail', kwargs={'pk': question.pk})
            return redirect(f'{question_url}?page={answer_page}#answer-{answer.pk}')
    answers_page = paginate(Answer.objects.for_question(question), request, per_page=10)
    return render(request, 'questions/question_detail.html', {'question': question, 'answers_page': answers_page, 'answer_form': answer_form})


@login_required
def ask(request):
    form = AskQuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        question = form.save(author=request.user)
        return redirect(question.get_absolute_url())
    return render(request, 'questions/ask.html', {'form': form})
