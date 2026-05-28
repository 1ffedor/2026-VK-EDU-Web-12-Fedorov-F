from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F

from .models import Question


def search_questions(query, limit=8):
    query = query.strip()
    if len(query) < 2:
        return []
    search_query = SearchQuery(query, config='russian')
    vector = SearchVector('title', weight='A', config='russian') + SearchVector('text', weight='B', config='russian')
    return list(
        Question.objects.annotate(
            rank=SearchRank(vector, search_query),
            search=vector,
        )
        .filter(search=search_query)
        .order_by(F('rank').desc(nulls_last=True), '-created_at')[:limit]
    )
