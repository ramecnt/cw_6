from datetime import datetime

import pytz
from django.db import models

from cw_6 import settings

FREQUENCY_CHOICES = [
    ('daily', 'ежедневно'),
    ('weekly', 'еженедельно'),
    ('monthly', 'ежемесячно'),
]

STATUS_CHOICES = [
    ('finished', 'закончена'),
    ('created', 'создана'),
    ('started', 'запущена')
]

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="почта")
    full_name = models.CharField(max_length=120, verbose_name="ФИО")
    commentary = models.CharField(max_length=250, verbose_name="комментарий")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        **NULLABLE
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Message(models.Model):
    theme = models.CharField(max_length=100, verbose_name='тема')
    text = models.CharField(max_length=500, verbose_name='тело сообщения')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        **NULLABLE
    )

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    start_sending = models.DateTimeField(verbose_name='дата начала рассылки')
    end_sending = models.DateTimeField(verbose_name='дата окончания рассылки')
    frequency = models.CharField(choices=FREQUENCY_CHOICES, verbose_name='частота отправки')
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='статус')
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='сообщение',
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name='клиенты',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        **NULLABLE
    )

    def __str__(self):
        return f'Рассылка {self.start_sending} - {self.end_sending}'

    def save(self, *args, **kwargs):
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)

        if current_datetime < self.start_sending:
            self.status = 'created'
        elif self.start_sending <= current_datetime <= self.end_sending:
            self.status = 'started'
        else:
            self.status = 'finished'

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class AttemptMailing(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата последней попытки')
    status = models.BooleanField(default=True, verbose_name='статус')
    server_response = models.CharField(max_length=100, verbose_name='ответ сервера')
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='рассылка'
    )

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылок'


class Blog(models.Model):

    heading = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name="картинка")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    views = models.IntegerField(verbose_name="количество просмотров", default=0)

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = ('heading',)
