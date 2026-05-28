from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .centrifugo import publish, question_channel
from .models import Answer
from .sidebar_cache import (
    compute_best_members,
    compute_popular_tags,
    store_best_members,
    store_popular_tags,
)


@shared_task
def refresh_popular_tags_cache():
    store_popular_tags(compute_popular_tags())


@shared_task
def refresh_best_members_cache():
    store_best_members(compute_best_members())


@shared_task
def publish_new_answer_event(answer_id):
    answer = Answer.objects.select_related('question').get(pk=answer_id)
    publish(
        question_channel(answer.question_id),
        {
            'type': 'new_answer',
            'answer_id': answer.pk,
            'question_id': answer.question_id,
        },
    )


@shared_task
def send_new_answer_email(answer_id):
    answer = Answer.objects.select_related('question', 'question__author').get(pk=answer_id)
    question = answer.question
    if question.author_id == answer.author_id or not question.author.email:
        return
    subject = f'Новый ответ на вопрос: {question.title}'
    message = (
        f'На ваш вопрос «{question.title}» ответил {answer.author.username}.\n\n'
        f'Текст ответа:\n{answer.text}\n\n'
        f'Ссылка: {settings.SITE_URL.rstrip("/")}/question/{question.pk}/'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [question.author.email],
        fail_silently=False,
    )


@shared_task
def notify_new_answer(answer_id):
    publish_new_answer_event.delay(answer_id)
    send_new_answer_email.delay(answer_id)
