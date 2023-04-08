from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import BasePermission
from tasks.api.serializers import TaskRetrieveModifySerializer, TaskCreateSerializer, CommentSerializer, \
    AdminAcceptDeclineTaskSerializer, TaskReclaimSerializer
from tasks.models import Task, Comment


class Tested(ListAPIView):
    serializer_class = TaskCreateSerializer
    queryset = Task.objects.all()


class IsOrdinaryUser(BasePermission):
    """selects only logged in users who are not staff"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff


class TasksViewSet(viewsets.ModelViewSet):
    """displays, creates and modifies user tasks"""
    queryset = Task.objects.all()
    permission_classes = [IsOrdinaryUser]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        return super().get_queryset()\
            .filter(author=self.request.user)\
            .filter(is_finally_rejected=False)

    def get_serializer_class(self):
        """triggers the needed serializer based on http method"""
        if self.action in ['list', 'partial_update']:
            return TaskRetrieveModifySerializer
        elif self.action in ['create']:
            return TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskReclaimAPIView(UpdateAPIView):
    """
    changes status to reclaimed for declined tasks, sets is_reclaimed to True
    and gives error if required to set is_reclaimed to False
    """
    serializer_class = TaskReclaimSerializer
    queryset = Task.objects.all()
    permission_classes = [IsOrdinaryUser]


class AddCommentAPIView(CreateAPIView):
    """adds comment to a task by user or admin"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdminTasksListAPIView(ListAPIView):
    """shows all admin tasks except for declined"""
    queryset = Task.objects.all()
    serializer_class = TaskRetrieveModifySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Task.objects.filter(status=Task.Status.IN_PROGRESS)


class AdminReClaimedTasksAPIView(AdminTasksListAPIView):
    """shows only reclaimed tasks"""

    def get_queryset(self):
        return Task.objects\
            .filter(status=Task.Status.DECLINED)\
            .filter(is_reclaimed=True)\
            .filter(is_finally_rejected=False)


class AdminAcceptDeclineTaskAPIView(UpdateAPIView):
    """handles the acceptance or decline of user's task"""
    serializer_class = AdminAcceptDeclineTaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAdminUser]


