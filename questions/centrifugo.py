import time

import jwt
import requests
from django.conf import settings


def question_channel(question_id):
    return f'{settings.CENTRIFUGO_NAMESPACE}:question_{question_id}'


def make_connection_token(user_id=None):
    payload = {
        'sub': str(user_id) if user_id else '',
        'exp': int(time.time()) + 3600,
    }
    token = jwt.encode(payload, settings.CENTRIFUGO_TOKEN_SECRET, algorithm='HS256')
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token


def publish(channel, data):
    url = f'{settings.CENTRIFUGO_API_URL.rstrip("/")}/api/publish'
    response = requests.post(
        url,
        json={'channel': channel, 'data': data},
        headers={
            'Content-Type': 'application/json',
            'X-API-Key': settings.CENTRIFUGO_API_KEY,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()
