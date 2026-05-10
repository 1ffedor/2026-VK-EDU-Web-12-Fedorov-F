from django.conf import settings
from django.db import models
from django.db.models import Count, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse


def votes_noun(value):
    n = abs(int(value)) % 100
    if 11 <= n <= 14:
        return 'голосов'
    m = n % 10
    if m == 1:
        return 'голос'
    if 2 <= m <= 4:
        return 'голоса'
    return 'голосов'


def answers_noun(value):
    n = abs(int(value)) % 100
    if 11 <= n <= 14:
        return 'ответов'
    m = n % 10
    if m == 1:
        return 'ответ'
    if 2 <= m <= 4:
        return 'ответа'
    return 'ответов'


class QuestionQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related('author', 'author__profile').prefetch_related('tags')

    def with_stats(self):
        return self.annotate(
            rating=Coalesce(Sum('question_likes__value'), Value(0), output_field=IntegerField()),
            answers_total=Count('answers', distinct=True),
        )

    def new(self):
        return self.with_related().with_stats().order_by('-created_at')

    def hot(self):
        return self.with_related().with_stats().order_by('-rating', '-created_at')

    def by_tag(self, slug):
        return self.with_related().with_stats().filter(tags__slug=slug).distinct().order_by('-created_at')


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def new(self):
        return self.get_queryset().new()

    def hot(self):
        return self.get_queryset().hot()

    def by_tag(self, slug):
        return self.get_queryset().by_tag(slug)

    def with_related(self):
        return self.get_queryset().with_related().with_stats()


class AnswerQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related('author', 'author__profile')

    def with_stats(self):
        return self.annotate(
            rating=Coalesce(Sum('answer_likes__value'), Value(0), output_field=IntegerField()),
        )


class AnswerManager(models.Manager):
    def get_queryset(self):
        return AnswerQuerySet(self.model, using=self._db)

    def for_question(self, question):
        return self.get_queryset().with_related().with_stats().filter(question=question).order_by('created_at')


class Tag(models.Model):
    name = models.CharField('название', max_length=64, unique=True)
    slug = models.SlugField('slug', max_length=64, unique=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField('заголовок', max_length=255)
    text = models.TextField('текст')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='автор',
    )
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name='теги', blank=True)
    views_count = models.PositiveIntegerField('просмотры', default=0)
    created_at = models.DateTimeField('создан', auto_now_add=True)
    updated_at = models.DateTimeField('обновлен', auto_now=True)

    objects = QuestionManager()

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})

    @property
    def votes(self):
        return getattr(self, 'rating', 0) or 0

    @property
    def votes_noun(self):
        return votes_noun(self.votes)

    @property
    def answers_label(self):
        total = getattr(self, 'answers_total', 0) or 0
        return f'{total} {answers_noun(total)}'

    @property
    def views_label(self):
        if self.views_count >= 1000:
            return f'{self.views_count // 1000}k показов'
        return f'{self.views_count} показов'

    @property
    def author_rep(self):
        profile = getattr(self.author, 'profile', None)
        return str(profile.rating) if profile else ''


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='вопрос',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='автор',
    )
    text = models.TextField('текст')
    is_correct = models.BooleanField('правильный', default=False)
    created_at = models.DateTimeField('создан', auto_now_add=True)

    objects = AnswerManager()

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
        ordering = ['created_at']

    def __str__(self):
        return f'Ответ #{self.pk}'

    @property
    def votes(self):
        return getattr(self, 'rating', 0) or 0


class QuestionLike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUES = (
        (LIKE, 'лайк'),
        (DISLIKE, 'дизлайк'),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes', verbose_name='вопрос')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_likes', verbose_name='пользователь')
    value = models.SmallIntegerField('оценка', choices=VALUES, default=LIKE)
    created_at = models.DateTimeField('создан', auto_now_add=True)

    class Meta:
        verbose_name = 'оценка вопроса'
        verbose_name_plural = 'оценки вопросов'
        unique_together = ('question', 'user')


class AnswerLike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUES = (
        (LIKE, 'лайк'),
        (DISLIKE, 'дизлайк'),
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes', verbose_name='ответ')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answer_likes', verbose_name='пользователь')
    value = models.SmallIntegerField('оценка', choices=VALUES, default=LIKE)
    created_at = models.DateTimeField('создан', auto_now_add=True)

    class Meta:
        verbose_name = 'оценка ответа'
        verbose_name_plural = 'оценки ответов'
        unique_together = ('answer', 'user')
