from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='пользователь',
    )
    nickname = models.CharField('ник', max_length=64, blank=True)
    avatar = models.ImageField('аватар', upload_to='avatars/', blank=True, null=True)
    rating = models.IntegerField('рейтинг', default=0)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.nickname or self.user.username
