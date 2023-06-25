from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('content', 'note', 'start', 'finish', 'owner', 'assignee', 'priority', 'status')
        widgets = {
            'owner' : forms.HiddenInput(),
            'start' : DateInput(),
            'finish' : DateInput(),
        }


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = models.TaskComment
        fields = ('content', 'task', 'commenter')
        widgets = {
            'task' : forms.HiddenInput(),
            'commenter' : forms.HiddenInput(),
        }
