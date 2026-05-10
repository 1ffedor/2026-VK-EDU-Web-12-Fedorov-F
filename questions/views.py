from django.shortcuts import get_object_or_404, render

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
    answers_page = paginate(Answer.objects.for_question(question), request, per_page=10)
    return render(request, 'questions/question_detail.html', {'question': question, 'answers_page': answers_page})


def ask(request):
    return render(request, 'questions/ask.html')
