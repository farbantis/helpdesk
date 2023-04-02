from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from tasks.api.serializers import TaskRetrieveModifySerializer, TaskCreateSerializer, CommentCreateSerializer, \
    AdminAcceptDeclineTaskSerializer
from tasks.models import Task, Comment


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        return super(TasksViewSet, self).get_queryset()\
            .filter(author=self.request.user)\
            .filter(is_finally_rejected=False)

    def get_serializer_class(self):
        print(f'self action is {self.action}')
        if self.action in ['update', 'list', 'partial_update']:
            return TaskRetrieveModifySerializer
        elif self.action in ['create']:
            return TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AddCommentAPIView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdminTasksListAPIView(ListAPIView):
    #queryset = super(AdminTasksListAPIView).get_queryset().filter(is_finally_rejected=False).filter(is_reclaimed = False)

    def get_queryset(self):
        return Task.objects.all()


class AdminAcceptDeclineTaskAPIView(UpdateAPIView):
    serializer_class = AdminAcceptDeclineTaskSerializer
    queryset = Task.objects.all()


class AdminReClaimedTasksAPIView(AdminTasksListAPIView):

    def get_queryset(self):
        return Task.objects.filter(is_reclaimed=True).filter(is_finally_rejected=False)

