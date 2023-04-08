from rest_framework import serializers
from tasks.models import Task, Comment, ReasonsToDecline


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'task', 'text_of_comment')

    def validate(self, attrs):
        """checks if the task is active to add comment"""
        print(f'task is {attrs}')
        task = attrs['task']
        if task.status != Task.Status.IN_PROGRESS:
            raise serializers.ValidationError('comments are available to tasks in progress only')
        return attrs


class TaskRetrieveModifySerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Task
        fields = (
        'id', 'author', 'title', 'message', 'status', 'priority', 'is_reclaimed', 'is_finally_rejected', 'comments'
        )
        read_only_fields = ('id', 'author', 'title', 'status', 'is_reclaimed', 'is_finally_rejected')


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'message', 'priority')


class TaskReclaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('is_reclaimed', )

    def validate_task(self, value):
        print(f'validating reclaim serializer value is {value}')
        task = self.instance
        if not value or task.status != Task.Status.DECLINED:
            serializers.ValidationError('invalid data')


class ReasonToDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonsToDecline
        fields = ('task', 'reason', )


class AdminAcceptDeclineTaskSerializer(serializers.ModelSerializer):
    reason = ReasonToDeclineSerializer

    class Meta:
        model = Task
        fields = ('id', 'status', )

    def validate(self, data):
        task = self.instance
        status = data.get('status')
        reason = data.get('reason')
        print(f'validating, task, status, reason is {task}, {status}, {reason}') # task text, D, None
        print(f'task.status = {task.status}')  # D
        if (task.status != Task.Status.IN_PROGRESS) and (not task.is_reclaimed):
            raise serializers.ValidationError(f'It is not allowed to change status of {task.status}')
        if status not in (Task.Status.DECLINED, Task.Status.CONFIRMED):
            raise serializers.ValidationError('Status doesnt exist')
        if task.status == Task.Status.DECLINED and not reason:
            raise serializers.ValidationError('reason is required if task is declined')



