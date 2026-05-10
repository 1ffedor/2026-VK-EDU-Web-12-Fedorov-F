# Сервис: Вопрос? Ответ!

## запуск локально

1) создайте `.env.local` на основе `.env.local.example`
2) поднимите postgres локально
3) запустите:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py fill_db 100
python manage.py createsuperuser
python manage.py runserver
```

в браузере: **http://127.0.0.1:8000/**
админка: **http://127.0.0.1:8000/admin/**

## запуск через docker

1) создайте `.env.docker` на основе `.env.docker.example`
2) запустите:

```bash
docker compose up --build
```

в другом окне:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py fill_db 100
docker compose exec web python manage.py createsuperuser
```

## страницы и роуты

- `index` - `/` - список новых вопросов
- `hot` - `/hot/` - список лучших вопросов
- `tag` - `/tag/<slug>/` - список вопросов по тегу
- `question_detail` - `/question/<id>/` - страница вопроса и ответы
- `ask` - `/ask/` - форма создания вопроса
- `login` - `/login/` - форма входа
- `signup` - `/signup/` - форма регистрации
- `profile` - `/profile/` - форма профиля

## что сделано в дз1 и дз2

- верстка страниц и общая структура шаблонов
- именованные url и шаблонные переходы через `{% url %}`
- пагинация через `paginate(objects_list, request, per_page=10)`
- requirements, dockerfile, docker-compose, readme

## что сделано в дз3

- модели `Profile`, `Question`, `Answer`, `Tag`, `QuestionLike`, `AnswerLike`
- ограничения от накрутки лайков через `unique_together`
- менеджер вопросов с выборками `new`, `hot`, `by_tag`
- админка `/admin/` с list_display, search_fields, list_filter, inline
- inline профиля в пользователе и inline ответов в вопросе
- read-only вывод данных из бд на списки и страницу вопроса
- 404 для несуществующего вопроса
- пустые состояния в списке вопросов и ответов
- management command `python manage.py fill_db [ratio]`
- postgres-конфиг через env и docker compose
- `django-debug-toolbar` только при `DEBUG=True`