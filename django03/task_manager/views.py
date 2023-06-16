from django.http import HttpResponse
from django.shortcuts import render
from . models import Task, TaskComment

def index(request):
    num_tasks = Task.objects.all().count()

    # To dictionary
    context = {
        'num_tasks' : num_tasks,
    }

    return render(request, 'task_manager/index.html', context)
