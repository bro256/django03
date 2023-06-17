from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
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
    paginate_by = 2
    template_name = "task_manager/task_list.html"


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/task_form.html'
    success_url = reverse_lazy('assignee_tasks')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        return context
    
    # Checks that the user passes the given test
    def test_func(self):
        obj = self.get_object()
        print(obj.assignee.all())
        if obj.owner == self.request.user:
            return True
        else:
            for assignee in obj.assignee.all():
                print("assignee: ", assignee)
                print("user: ", self.request.user)
                if assignee == self.request.user:
                    return True
                else:
                    return False

        # return obj.owner == self.request.user