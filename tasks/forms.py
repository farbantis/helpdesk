from django import forms
from tasks.models import Task, Comment, ReasonsToDecline


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'message', 'priority']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text_of_comment',)
        widgets = {
            'text_of_comment': forms.Textarea(attrs={'rows': 1, 'cols': 50})
        }


class AdminAcceptDenyForm(forms.ModelForm):
    DECISION_CHOICES = [
        ('', 'Make a choice'),
        (True, 'Accept'),
        (False, 'Decline'),
    ]
    decision = forms.ChoiceField(choices=DECISION_CHOICES)

    class Meta:
        model = ReasonsToDecline
        fields = ('reason', 'decision')
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 1, 'cols': 50, 'required': False})
        }
