from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/update/<int:pk>/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
]
