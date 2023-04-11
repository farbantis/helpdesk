from rest_framework import serializers
from account.models import User
from tasks.models import Task, Comment, ReasonsToDecline


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'task', 'text_of_comment')

    def get_author(self, object):
        return object.author.username

    def validate(self, attrs):
        """checks if the task is active to add comment"""
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

    def validate(self, attrs):
        task = self.instance
        if task.status != Task.Status.DECLINED:
            raise serializers.ValidationError('invalid data')
        return attrs


class ReasonToDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonsToDecline
        fields = ('reason', )


class AdminAcceptDeclineTaskSerializer(serializers.ModelSerializer):
    reason = ReasonToDeclineSerializer(required=False)

    class Meta:
        model = Task
        fields = ('id', 'status', 'reason')

    def validate(self, data):
        task = self.instance
        status = data.get('status')
        reason = data.get('reason')
        if (task.status != Task.Status.IN_PROGRESS) and (not task.is_reclaimed):
            raise serializers.ValidationError('It is not allowed to change this status')
        if status not in (Task.Status.DECLINED, Task.Status.CONFIRMED):
            raise serializers.ValidationError('You can either accept or decline')
        if (status == Task.Status.DECLINED) and (not reason) and (not task.is_reclaimed):
            raise serializers.ValidationError('reason is required if task is declined')
        return data

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        reason = validated_data.get('reason')
        task = instance
        if reason:
            reason = reason.get('reason')
            ReasonsToDecline.objects.create(task=task, reason=reason)
        if task.is_reclaimed:
            task.is_finally_rejected = True
            task.save()
        instance.save()
        return instance



