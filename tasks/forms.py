from django import forms
from tasks.models import Task, Comment


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'message', 'priority']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text_of_comment', )
