from django.urls import path
from .views import TasksView, TaskCreateView, TaskEditView, AdminTasksView, AdminTasksDeclinedView, TaskRestoreView

app_name = 'task'

urlpatterns = [
    path('', TasksView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('edit/<int:pk>/', TaskEditView.as_view(), name='task_edit'),
    path('task_restore/<int:pk>/', TaskRestoreView.as_view(), name='task_restore'),
    path('admin_tasks/', AdminTasksView.as_view(), name='admin_task'),
    path('admin_tasks_declined/', AdminTasksDeclinedView.as_view(), name='admin_task_declined')
]
