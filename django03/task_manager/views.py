from django.http import HttpResponse
from django.shortcuts import render
from . models import Task, TaskComment
from django.views import generic


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

    

