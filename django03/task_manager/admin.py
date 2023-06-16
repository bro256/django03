from django.contrib import admin
from . import models

class TaskAdmin(admin.ModelAdmin):
    list_display = ('content', 'start', 'finish', 'is_overdue', 'owner', 'priority', 'status', 'created_at')
    list_filter = ('owner',)

class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at',)

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.TaskComment, TaskCommentAdmin)