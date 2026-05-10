from django import forms
from django.db import transaction
from django.utils.text import slugify

from .models import Answer, Question, Tag


class AskQuestionForm(forms.ModelForm):
    tags = forms.CharField(label='Теги', required=False, help_text='Через запятую: django, python, css')

    class Meta:
        model = Question
        fields = ('title', 'text')
        labels = {
            'title': 'Заголовок',
            'text': 'Текст вопроса',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control rounded-pill', 'placeholder': 'Коротко о сути вопроса'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'rows': 8, 'placeholder': 'Опишите проблему максимально подробно...'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control rounded-pill', 'placeholder': 'css, html, python'})

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        parsed = []
        for tag in raw.split(','):
            item = tag.strip()
            if item:
                parsed.append(item[:64])
        unique = list(dict.fromkeys(parsed))
        if len(unique) > 10:
            raise forms.ValidationError('Можно указать не более 10 тегов')
        return unique

    @transaction.atomic
    def save(self, author, commit=True):
        question = super().save(commit=False)
        question.author = author
        if commit:
            question.save()
            tags = []
            for name in self.cleaned_data.get('tags', []):
                slug = slugify(name, allow_unicode=False)[:64] or f'tag-{abs(hash(name)) % 10**8}'
                tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
                if tag.name != name:
                    tag.name = name
                    tag.save(update_fields=['name'])
                tags.append(tag)
            if tags:
                question.tags.set(tags)
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        labels = {'text': 'Ваш ответ'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control mb-3', 'rows': 6, 'placeholder': 'Введите ответ...'})

    def save(self, author, question, commit=True):
        answer = super().save(commit=False)
        answer.author = author
        answer.question = question
        if commit:
            answer.save()
        return answer
