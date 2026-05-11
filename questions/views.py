from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.decorators.http import require_POST

from .forms import AnswerForm, AskQuestionForm, CorrectAnswerForm, VoteForm
from .models import Answer, AnswerLike, Question, QuestionLike, Tag
from .utils import paginate


def _render_list(request, queryset, page_title, list_tab, tag_slug=''):
    page = paginate(queryset, request)
    voted_question_ids = set()
    if request.user.is_authenticated:
        question_ids = [q.id for q in page.object_list]
        voted_question_ids = set(
            QuestionLike.objects.filter(user=request.user, question_id__in=question_ids).values_list('question_id', flat=True)
        )
    return render(
        request,
        'questions/list.html',
        {
            'page': page,
            'page_title': page_title,
            'list_tab': list_tab,
            'tag': tag_slug,
            'voted_question_ids': voted_question_ids,
        },
    )


def _json_error(message, status=400, login_url=None):
    payload = {'ok': False, 'error': message}
    if login_url:
        payload['login_url'] = login_url
    return JsonResponse(payload, status=status)


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
    voted_question_ids = set()
    voted_answer_ids = set()
    if request.user.is_authenticated:
        if QuestionLike.objects.filter(user=request.user, question=question).exists():
            voted_question_ids.add(question.id)
        answer_ids = [a.id for a in answers_page.object_list]
        voted_answer_ids = set(
            AnswerLike.objects.filter(user=request.user, answer_id__in=answer_ids).values_list('answer_id', flat=True)
        )
    return render(
        request,
        'questions/question_detail.html',
        {
            'question': question,
            'answers_page': answers_page,
            'answer_form': answer_form,
            'voted_question_ids': voted_question_ids,
            'voted_answer_ids': voted_answer_ids,
        },
    )


@login_required
def ask(request):
    form = AskQuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        question = form.save(author=request.user)
        return redirect(question.get_absolute_url())
    return render(request, 'questions/ask.html', {'form': form})


@require_POST
def vote_question(request):
    if not request.user.is_authenticated:
        login_url = f"{reverse('login')}?{urlencode({'next': request.META.get('HTTP_REFERER', '/')})}"
        return _json_error('нужна авторизация', status=403, login_url=login_url)
    form = VoteForm(request.POST)
    if not form.is_valid():
        return _json_error('невалидные параметры')
    question = get_object_or_404(Question, pk=form.cleaned_data['target_id'])
    vote_value = form.cleaned_data['vote_type']
    if QuestionLike.objects.filter(question=question, user=request.user).exists():
        return _json_error('вы уже голосовали')
    QuestionLike.objects.create(question=question, user=request.user, value=vote_value)
    total_rating = QuestionLike.objects.filter(question=question).aggregate(sum=Sum('value'))['sum'] or 0
    return JsonResponse({'ok': True, 'rating': total_rating, 'target_id': question.pk})


@require_POST
def vote_answer(request):
    if not request.user.is_authenticated:
        login_url = f"{reverse('login')}?{urlencode({'next': request.META.get('HTTP_REFERER', '/')})}"
        return _json_error('нужна авторизация', status=403, login_url=login_url)
    form = VoteForm(request.POST)
    if not form.is_valid():
        return _json_error('невалидные параметры')
    answer = get_object_or_404(Answer, pk=form.cleaned_data['target_id'])
    vote_value = form.cleaned_data['vote_type']
    if AnswerLike.objects.filter(answer=answer, user=request.user).exists():
        return _json_error('вы уже голосовали')
    AnswerLike.objects.create(answer=answer, user=request.user, value=vote_value)
    total_rating = AnswerLike.objects.filter(answer=answer).aggregate(sum=Sum('value'))['sum'] or 0
    return JsonResponse({'ok': True, 'rating': total_rating, 'target_id': answer.pk})


@require_POST
def mark_correct_answer(request):
    if not request.user.is_authenticated:
        login_url = f"{reverse('login')}?{urlencode({'next': request.META.get('HTTP_REFERER', '/')})}"
        return _json_error('нужна авторизация', status=403, login_url=login_url)
    form = CorrectAnswerForm(request.POST)
    if not form.is_valid():
        return _json_error('невалидные параметры')
    question = get_object_or_404(Question, pk=form.cleaned_data['question_id'])
    if question.author_id != request.user.id:
        return _json_error('только автор вопроса может выбрать правильный ответ', status=403)
    answer = form.cleaned_data['answer_obj']
    Answer.objects.filter(question=question, is_correct=True).update(is_correct=False)
    Answer.objects.filter(pk=answer.pk).update(is_correct=True)
    return JsonResponse({'ok': True, 'question_id': question.pk, 'answer_id': answer.pk})
