# Сервис: Вопрос? Ответ!

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

В браузере: **http://127.0.0.1:8000/**

Скопируйте `.env.example` в `.env` и задайте `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.

## Docker Compose

```bash
docker compose up --build
```

## Страницы и маршруты

- `index` - `/` - главная, новые вопросы
- `hot` - `/hot/` - вопросы по убыванию голосов
- `tag` - `/tag/<slug>/` - вопросы с тегом (например `/tag/python/`)
- `question_detail` - `/question/<id>/` - страница одного вопроса и ответов
- `ask` - `/ask/` - форма создания вопроса
- `login` - `/login/` - форма входа
- `signup` - `/signup/` - регистрация
- `profile` - `/profile/` - редактирование профиля
