from django import forms

class ScheduleForm(forms.Form):
    schedule = forms.CharField(label='New Schedule (CRON expression)')
