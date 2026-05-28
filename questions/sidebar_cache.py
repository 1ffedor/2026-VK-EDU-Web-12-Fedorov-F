from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import Answer, AnswerLike, Question, QuestionLike, Tag

User = get_user_model()


def compute_popular_tags():
    since = timezone.now() - timedelta(days=90)
    tags = (
        Tag.objects.filter(questions__created_at__gte=since)
        .annotate(questions_count=Count('questions', distinct=True))
        .order_by('-questions_count', 'name')[:10]
    )
    return [
        {'name': tag.name, 'slug': tag.slug, 'count': tag.questions_count}
        for tag in tags
    ]


def compute_best_members():
    since = timezone.now() - timedelta(days=7)
    scores = {}

    question_rows = (
        Question.objects.filter(created_at__gte=since)
        .values('author_id', 'author__username')
        .annotate(score=Coalesce(Sum('question_likes__value'), Value(0)))
        .order_by('-score')[:50]
    )
    for row in question_rows:
        user_id = row['author_id']
        scores[user_id] = {
            'user_id': user_id,
            'username': row['author__username'],
            'score': row['score'] or 0,
        }

    answer_rows = (
        Answer.objects.filter(created_at__gte=since)
        .values('author_id', 'author__username')
        .annotate(score=Coalesce(Sum('answer_likes__value'), Value(0)))
        .order_by('-score')[:50]
    )
    for row in answer_rows:
        user_id = row['author_id']
        entry = scores.get(user_id)
        if entry:
            entry['score'] += row['score'] or 0
        else:
            scores[user_id] = {
                'user_id': user_id,
                'username': row['author__username'],
                'score': row['score'] or 0,
            }

    top = sorted(scores.values(), key=lambda item: item['score'], reverse=True)[:10]
    user_ids = [item['user_id'] for item in top]
    users = {
        user.pk: user
        for user in User.objects.filter(pk__in=user_ids).select_related('profile')
    }
    result = []
    for item in top:
        user = users.get(item['user_id'])
        profile = getattr(user, 'profile', None) if user else None
        avatar_url = profile.avatar.url if profile and profile.avatar else ''
        result.append(
            {
                'user_id': item['user_id'],
                'username': item['username'],
                'score': item['score'],
                'avatar_url': avatar_url,
            }
        )
    return result


def get_popular_tags():
    data = cache.get(settings.CACHE_KEY_POPULAR_TAGS)
    if data is None:
        data = compute_popular_tags()
        cache.set(settings.CACHE_KEY_POPULAR_TAGS, data, timeout=None)
    return data


def get_best_members():
    data = cache.get(settings.CACHE_KEY_BEST_MEMBERS)
    if data is None:
        data = compute_best_members()
        cache.set(settings.CACHE_KEY_BEST_MEMBERS, data, timeout=None)
    return data


def store_popular_tags(data):
    cache.set(settings.CACHE_KEY_POPULAR_TAGS, data, timeout=None)


def store_best_members(data):
    cache.set(settings.CACHE_KEY_BEST_MEMBERS, data, timeout=None)
