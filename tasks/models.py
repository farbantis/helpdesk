from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class Task(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'C', _('confirmed')
        DECLINED = 'D', _('declined')
        IN_PROGRESS = 'P', _('in progress')

    class Priority(models.TextChoices):
        LOW = 'L', _('low')
        MEDIUM = 'M', _('medium')
        HIGH = 'H', _('high')

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, default='')
    message = models.TextField()
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.IN_PROGRESS)
    priority = models.CharField(max_length=1, choices=Priority.choices, default=Priority.LOW)
    is_reclaimed = models.BooleanField(default=False)
    is_finally_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}, {self.status}'

    @property
    def is_declined(self):
        return self.status == self.Status.DECLINED

    @property
    def get_status(self):
        return dict(self.Status.choices)[self.status]

    @property
    def get_priority(self):
        return dict(self.Priority.choices)[self.priority]


class ReasonsToDecline(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)

    def __str__(self):
        return str(self.task)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text_of_comment = models.TextField(verbose_name='Your comment')
    date_of_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} commented {self.task}'
