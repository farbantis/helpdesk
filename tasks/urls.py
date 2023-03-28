from django.urls import path
from .views import TasksView, TaskCreateView, TaskEditView

app_name = 'task'

urlpatterns = [
    path('', TasksView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('edit/<int:pk>/', TaskEditView.as_view(), name='task_edit'),
]
