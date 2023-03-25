from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class Task(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'C', _('confirmed')
        DECLINED = 'D', _('declined')
        IN_PROGRESS = 'P', _('in progress')

    class Importance(models.TextChoices):
        LOW = 'L', _('low')
        MEDIUM = 'M', _('medium')
        HIGH = 'H', _('high')

    author = models.OneToOneField(User, on_delete=models.PROTECT)
    message = models.TextField()
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.IN_PROGRESS)
    importance = models.CharField(max_length=1, choices=Importance.choices, default=Importance.LOW)
    #comments = models.