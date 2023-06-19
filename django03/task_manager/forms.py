from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type = 'date'

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('content', 'start', 'finish', 'owner', 'assignee', 'priority', 'status')
        widgets = {
            'owner' : forms.HiddenInput(),
            'start' : DateInput(),
            'finish' : DateInput(),
        }
