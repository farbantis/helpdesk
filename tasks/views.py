from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from tasks.forms import TaskCreateForm, CommentForm, AdminAcceptDenyForm
from tasks.mixins import CreateCommentMixin
from tasks.models import Task, ReasonsToDecline


class TasksView(CreateCommentMixin, UserPassesTestMixin, ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    model = Task
    extra_context = {'form': CommentForm}

    def test_func(self):
        return not self.request.user.is_staff and self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('account:login')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).filter(is_reclaimed=False)

    def post(self, request):
        self.create_comment(request)
        return redirect('task:index')


class TaskRestoreView(View):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_reclaimed = True
        task.save()
        return redirect(reverse_lazy('task:index'))


class TaskCreateView(UserPassesTestMixin, CreateView):
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
            messages.add_message(request, messages.SUCCESS, 'task was created')
            return redirect('task:index')
        messages.add_message(request, messages.ERROR, 'there was an error while creating the task')
        return render(request, 'tasks/create_new_task.html', {'form': form})

    def test_func(self):
        return not self.request.user.is_staff and self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('account:login')


class TaskEditView(UserPassesTestMixin, UpdateView):
    template_name = 'tasks/edit_task.html'
    model = Task
    fields = ('message', 'priority')
    success_url = reverse_lazy('task:index')

    def test_func(self):
        return not self.request.user.is_staff and self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('account:login')


class AdminTasksView(CreateCommentMixin, UserPassesTestMixin, ListView):
    template_name = 'tasks/index_admin.html'
    context_object_name = 'tasks'
    model = Task
    extra_context = {'form_accept_deny': AdminAcceptDenyForm, 'form': CommentForm}
    permission_required = ('is_staff', )

    def get_queryset(self):
        return self.model.objects.filter(status=Task.Status.IN_PROGRESS).filter(is_reclaimed=False)

    def post(self, request):
        if 'text_of_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                self.create_comment(request)
        elif 'decision' in request.POST:
            form_accept_deny = AdminAcceptDenyForm(request.POST)
            if form_accept_deny.is_valid():
                cd = form_accept_deny.cleaned_data
                task = get_object_or_404(Task, pk=request.POST.get('task_id'))
                if cd['decision'] == 'True':
                    task.status = Task.Status.CONFIRMED
                    task.save()
                    messages.add_message(request, messages.SUCCESS, 'you confirmed the task')
                else:
                    reason = cd['reason']
                    if reason:
                        task.status = Task.Status.DECLINED
                        task.save()
                        ReasonsToDecline.objects.create(task_id=task.id, reason=reason)
                        messages.add_message(request, messages.SUCCESS, 'you declined the task')
                    else:
                        messages.add_message(request, messages.ERROR, 'You must indicate reason to decline')
        return redirect('task:admin_task')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('account:login')


class AdminTasksDeclinedView(AdminTasksView):
    """use to finally decline or accept reclaimed tasks, doesn't require comment to deny"""
    def get_queryset(self):
        return self.model.objects\
            .filter(status=Task.Status.DECLINED)\
            .filter(is_reclaimed=True)\
            .filter(is_finally_rejected=False)

    def post(self, request):
        form_accept_deny = AdminAcceptDenyForm(request.POST)
        if form_accept_deny.is_valid():
            cd = form_accept_deny.cleaned_data
            task = get_object_or_404(Task, pk=request.POST.get('task_id'))
            if cd['decision'] == 'True':
                task.status = Task.Status.CONFIRMED
                task.is_reclaimed = False
                task.save()
                messages.add_message(request, messages.SUCCESS, 'the task has been confirmed')
            else:
                task.is_finally_rejected = True
                task.save()
                messages.add_message(request, messages.SUCCESS, 'the task has been finally rejected')
        return redirect('task:admin_task_declined')
