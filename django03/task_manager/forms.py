from django import forms
from . import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('content', 'start', 'finish', 'owner', 'assignee', 'priority', 'status')
        widgets = {
            'owner' : forms.HiddenInput(),
        }
