from django.contrib import admin
from .models import Task, Comment, ReasonsToDecline


admin.site.register(Task)
admin.site.register(ReasonsToDecline)
admin.site.register(Comment)


