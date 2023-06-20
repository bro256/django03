from datetime import date, timedelta
from typing import Any, Dict, Optional
from typing import Any
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from . forms import TaskForm
from . models import Task, TaskComment



def index(request):
    num_tasks = Task.objects.all().count()

    # To dictionary
    context = {
        'num_tasks' : num_tasks,
    }

    return render(request, 'task_manager/index.html', context)

class TaskListView(generic.ListView):
    model = Task
    paginate_by = 20
    template_name = "task_manager/task_list.html"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner__username=user.username)

class UserTaskListView(generic.ListView):
    model = Task
    paginate_by = 20
    template_name = "task_manager/user_task_list.html"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee__username=user.username)


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"


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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        return context
    
    # Checks that the user passes the given test
    def test_func(self):
        obj = self.get_object()
        if obj.owner == self.request.user:
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

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.owner == self.request.user