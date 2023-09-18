from django import forms

class ScheduleForm(forms.Form):
    
    schedule = forms.CharField(
        label='Cron Schedule',
        max_length=100,
        help_text='Enter a valid cron expression (e.g., "0 0 * * *")'
    )
