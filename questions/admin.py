from django.contrib import admin

from .models import Answer, AnswerLike, Question, QuestionLike, Tag


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    autocomplete_fields = ('author',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'views_count')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('created_at', 'tags')
    autocomplete_fields = ('author',)
    filter_horizontal = ('tags',)
    inlines = (AnswerInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author').prefetch_related('tags')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'is_correct', 'created_at')
    search_fields = ('text', 'author__username', 'question__title')
    list_filter = ('is_correct', 'created_at')
    autocomplete_fields = ('question', 'author')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question', 'author')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('question__title', 'user__username')
    autocomplete_fields = ('question', 'user')


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('answer__text', 'user__username')
    autocomplete_fields = ('answer', 'user')
