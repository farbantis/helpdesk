from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from tasks.forms import TaskCreateForm, CommentForm, DenyForm, DenyFormNoReason
from tasks.models import Task, Comment, ReasonsToDecline


def create_comment(request):
    Comment.objects.create(
        task=Task.objects.get(id=request.POST.get('task_id')),
        author=request.user,
        text_of_comment=request.POST.get('text_of_comment')
    )


class TasksView(UserPassesTestMixin, ListView):
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
        create_comment(request)
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
            messages.add_message(request, messages.SUCCESS, f'task was created')
            return redirect('task:index')
        else:
            messages.add_message(request, messages.ERROR, f'there was an error while creating the task')
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


class AdminTasksView(UserPassesTestMixin, ListView):
    template_name = 'tasks/index_admin.html'
    context_object_name = 'tasks'
    model = Task
    extra_context = {'form_deny': DenyForm, 'form': CommentForm, 'form_deny_no_reason': DenyFormNoReason}
    permission_required = ('is_staff', )

    def get_queryset(self):
        return self.model.objects.filter(status=Task.Status.IN_PROGRESS).filter(is_reclaimed=False)

    def post(self, request):
        if 'text_of_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                create_comment(request)
        elif 'decision' in request.POST:
            print('there is a decision...')
            form_deny = DenyForm(request.POST)
            if form_deny.is_valid():
                cd = form_deny.cleaned_data
                print(f'and it is {cd["decision"]}')
                task = Task.objects.get(id=request.POST.get('task_id'))
                if cd['decision'] == 'False':
                    ReasonsToDecline.objects.create(reason=cd['reason'], task=task)
                    task.status = Task.Status.DECLINED
                    task.save()
                else:
                    task.status = Task.Status.CONFIRMED
                    task.save()
        return redirect('task:admin_task')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('account:login')


class AdminTasksDeclinedView(AdminTasksView):

    def get_queryset(self):
        return self.model.objects.filter(is_reclaimed=True).filter(is_finally_rejected=False)

    def post(self, request):
        form_deny_no_reason = DenyFormNoReason(request.POST)
        print('within needed form')
        if form_deny_no_reason.is_valid():
            print('form was valid')
            cd = form_deny_no_reason.cleaned_data
            task = Task.objects.get(id=request.POST.get('task_id'))
            if cd['decision'] == 'False':
                task.is_finally_rejected = True
                task.save()
            else:
                task.status = Task.Status.CONFIRMED
        return redirect('task:admin_task_declined')
