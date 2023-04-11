from tasks.models import Comment, Task


class CreateCommentMixin:
    """adds comments both for user and admin"""

    def create_comment(self, request):
        Comment.objects.create(
            task=Task.objects.get(id=request.POST.get('task_id')),
            author=request.user,
            text_of_comment=request.POST.get('text_of_comment')
        )
