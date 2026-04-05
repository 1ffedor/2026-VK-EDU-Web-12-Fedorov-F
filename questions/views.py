from django.shortcuts import render

from .stub_data import get_question_by_id, get_questions_for_tag, get_hot_questions, get_new_questions, votes_noun
from .utils import paginate


def _answers_heading(count):
    n = count % 100
    if 11 <= n <= 14:
        word = 'ответов'
    else:
        m = count % 10
        if m == 1:
            word = 'ответ'
        elif 2 <= m <= 4:
            word = 'ответа'
        else:
            word = 'ответов'
    return f'{count} {word}'


def _answers_for_question(pk):
    q = get_question_by_id(pk)
    if q and 'java' in [t.lower() for t in q['tags']]:
        return [
            {
                'id': 1,
                'votes': 15,
                'text': (
                    'Optional используется, потому что стрим может быть пустым. '
                    'Используйте `.orElseThrow()`, если уверены, что элемент есть, или `orElse` с запасным значением.'
                ),
                'author': 'senior',
                'time_ago': '2 часа назад',
                'is_correct': True,
            },
            {
                'id': 2,
                'votes': 3,
                'text': 'Если нужен не максимум, а «стрим дальше», смотрите в сторону операций над потоком до терминальной операции.',
                'author': 'java_fan',
                'time_ago': '1 час назад',
                'is_correct': False,
            },
        ]
    if q:
        return [
            {
                'id': 1,
                'votes': 5,
                'text': 'Короткий ответ-заглушка: детали зависят от версии стека и окружения, уточните в комментарии.',
                'author': 'community',
                'time_ago': '10 минут назад',
                'is_correct': False,
            },
        ]
    return []


def index(request):
    page = paginate(get_new_questions(), request)
    return render(
        request,
        'questions/list.html',
        {
            'page': page,
            'page_title': 'Все вопросы',
            'list_tab': 'new',
        },
    )


def hot(request):
    page = paginate(get_hot_questions(), request)
    return render(
        request,
        'questions/list.html',
        {
            'page': page,
            'page_title': 'Горячее',
            'list_tab': 'hot',
        },
    )


def tag(request, tag):
    filtered = get_questions_for_tag(tag)
    page = paginate(filtered, request)
    return render(
        request,
        'questions/list.html',
        {
            'page': page,
            'page_title': f'{tag}',
            'list_tab': 'tag',
            'tag': tag,
        },
    )


def question_detail(request, pk):
    question = get_question_by_id(pk)
    if question is None:
        question = {
            'id': pk,
            'title': f'Вопрос #{pk}',
            'text': 'Такого вопроса нет в демо-списке — это заглушка.',
            'author': 'system',
            'tags': ['django'],
            'votes': 0,
            'votes_noun': votes_noun(0),
            'views_label': '0 показов',
            'author_rep': '',
            'time_ago': '—',
        }
    answers = _answers_for_question(pk)
    return render(
        request,
        'questions/question_detail.html',
        {
            'question': question,
            'answers': answers,
            'answers_heading': _answers_heading(len(answers)),
        },
    )


def ask(request):
    return render(request, 'questions/ask.html')
