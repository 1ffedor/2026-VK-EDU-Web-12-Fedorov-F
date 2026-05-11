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