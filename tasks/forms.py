from django import forms
from django.core.exceptions import ValidationError
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


class DenyForm(forms.ModelForm):
    decision = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = ReasonsToDecline
        fields = ('reason', 'decision')
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 1, 'cols': 50})
        }

    def clean(self):
        if 'decision' in self.data:
            decision = self.data['decision']
            cd = super().clean()
            reason = cd['reason']
            if (decision == 'False') and (not reason):
                raise ValidationError('you should fill in the reason')


class DenyFormNoReason(forms.ModelForm):
    decision = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = ReasonsToDecline
        fields = ('decision', )

