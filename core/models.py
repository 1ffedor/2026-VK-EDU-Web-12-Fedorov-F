from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db import models


def profile_avatar_upload_to(instance, filename):
    ext = Path(filename).suffix.lower() or '.jpg'
    return f'avatars/{instance.user_id}/{uuid4().hex}{ext}'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='пользователь',
    )
    nickname = models.CharField('ник', max_length=64, blank=True)
    avatar = models.ImageField('аватар', upload_to=profile_avatar_upload_to, blank=True, null=True)
    rating = models.IntegerField('рейтинг', default=0)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.nickname or self.user.username
