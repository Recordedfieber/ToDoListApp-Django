from django import forms
from .models import TodoTask


class DateInput(forms.DateInput):
    input_type = 'date'


class TodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = ['task_title', 'task_priority', 'task_due_date', 'task_status']
        widgets = {
            'task_due_date': DateInput()
        }
    
