from datetime import date, timedelta
from typing import Any, Dict, Optional
from typing import Any
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from . forms import TaskForm
from . models import Task, TaskComment
from . forms import TaskCommentForm
from django.db.models import Count


def index(request):
    num_tasks = Task.objects.all().count()
    num_tasks_not_tarted = Task.objects.filter(status__exact=0).count

    # To dictionary
    context = {
        'num_tasks' : num_tasks,
        'num_tasks_not_tarted' : num_tasks_not_tarted,
    }

    return render(request, 'task_manager/index.html', context)

class TaskListView(generic.ListView):
    model = Task
    paginate_by = 20
    template_name = "task_manager/task_list.html"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(owner__username=user.username) | Q(assignee__username=user.username))
    
    # For calculation of tasks with different statuses for logged in user 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        task_counts = (
            Task.objects.filter(assignee=user)
            .values('status')
            .annotate(count=Count('status'))
        )
        # Convert status values to words
        for count in task_counts:
            count['status_display'] = Task.STATUS_CHOICES[count['status']][1]
        context['task_counts'] = task_counts
        return context

class UserTaskListView(generic.ListView):
    model = Task
    paginate_by = 20
    template_name = "task_manager/user_task_list.html"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee__username=user.username)


class TaskDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
    form_class = TaskCommentForm

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['task'] = self.get_object()
        initial['commenter'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.task = self.get_object()
        form.instance.commenter = self.request.user
        form.save()
        messages.success(self.request, _('Comment posted successfully!'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('task_detail', kwargs={'pk':self.get_object().pk})


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    
    def get_initial(self) -> Dict[str, Any]:
        # self.task = get_object_or_404(Task, id=self.request.GET.get('task_id'))
        initial = super().get_initial()
        initial['start'] = date.today()
        initial['finish'] = date.today() + timedelta(days=7)
        initial['status'] = 0
        initial['priority'] = 2
        initial['owner'] = self.request.user
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            initial['assignee'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _('Task created successfully!'))
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            form.fields['assignee'].initial = self.request.user.username
            form.fields['assignee'].widget = forms.HiddenInput()

        return form

    # Checks that the user passes the given test
    def test_func(self):
        return self.request.user.is_authenticated
                  

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.object.owner == self.request.user and not self.request.user.is_superuser:
            form.fields['assignee'].widget = forms.HiddenInput()

        elif self.object.owner != self.request.user and not self.request.user.is_superuser:
            # If user is superuser, exclude all fields except "status"
            for field_name in form.fields:
                if field_name != 'status':
                    form.fields[field_name].widget = forms.HiddenInput()

        return form
    
    def form_valid(self, form):
        messages.success(self.request, _('Task updated successfully!'))
        return super().form_valid(form)

    # Checks that the user passes the given test
    def test_func(self):
        obj = self.get_object()
        if obj.owner == self.request.user or obj.assignee == self.request.user:
            return True
        else:
            return False
            # for assignee in obj.assignee.all():
            #     if assignee == self.request.user:
            #         return True
            #     else:
            #         return False

        # return obj.owner == self.request.user

class TaskDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Task
    template_name = 'task_manager/task_delete.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, _('Task deleted successfully!'))
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.owner == self.request.user