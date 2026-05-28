# Сервис: Вопрос? Ответ!

## запуск локально

1) заполните `.env.local` на основе `.env.local.example`
2) поднимите postgres и redis локально
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

в отдельных окнах (для дз 6):

```bash
celery -A application worker -l info
celery -A application beat -l info --scheduler redbeat.RedBeatScheduler
```

опционально для realtime и email:

```bash
docker compose up centrifugo maildev
```

в браузере: **http://127.0.0.1:8000/**
админка: **http://127.0.0.1:8000/admin/**
maildev: **http://127.0.0.1:1080/**
centrifugo ws: **ws://127.0.0.1:8001/connection/websocket**

## запуск через docker

1) заполните `.env.docker` на основе `.env.docker.example`
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

сайт: **http://127.0.0.1:8000/**
админка: **http://127.0.0.1:8000/admin/**
maildev: **http://127.0.0.1:1080/**

## дз 6

- redis: cache django + broker celery + redbeat schedule (разные db)
- celery worker/beat: пересчет популярных тегов и топ пользователей в сайдбаре
- centrifugo: realtime новые ответы на странице вопроса
- maildev: email автору вопроса при новом ответе
- postgres full-text search: подсказки в поиске в шапке (debounce)
