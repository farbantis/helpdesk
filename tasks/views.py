from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from tasks.forms import TaskCreateForm, CommentForm
from tasks.models import Task, Comment


class TasksView(UserPassesTestMixin, ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    model = Task
    extra_context = {'form': CommentForm}
    #success_message = 'congratulations, you made a purchase'

    def test_func(self):
        return not self.request.user.is_staff and self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('account:login')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(TasksView, self).get_context_data()
    #     context['comments'] = Comment.objects.filter(task__author=self.request.user)
    #     return context

    def post(self, request):
        Comment.objects.create(
            task=Task.objects.get(id=request.POST.get('task_id')),
            author=request.user,
            text_of_comment=request.POST.get('text_of_comment')
        )
        return redirect('task:index')


class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/create_new_task.html'
    form_class = TaskCreateForm

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.author_id = request.user.id
            new_task.status = Task.Status.IN_PROGRESS
            new_task.save()
            #messages.add_message(request, messages.SUCCESS, f'user was created and granted {new_user.wallet}$')
            return redirect('task:index')
        return render(request, 'tasks/create_new_task.html', {'form': form})


class TaskEditView(UserPassesTestMixin, UpdateView):
    template_name = 'tasks/edit_task.html'
    model = Task
    fields = ('message', 'priority')
    success_url = reverse_lazy('task:index')

    def test_func(self):
        return not self.request.user.is_staff and self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('account:login')



