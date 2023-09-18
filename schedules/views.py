from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import TaskRecord
from .forms import ScheduleForm
from crontab import CronTab
from django.http import Http404
from croniter import croniter
from django.contrib import messages

import re

def is_valid_cron_expression(expression):
    cron_pattern = r'^\S+\s+\S+\s+\S+\s+\S+\s+\S+$'
    return re.match(cron_pattern, expression) is not None


class ScheduleView(View):
    template_name = 'property_backend/schedule.html'

    def get(self, request, task_id):
        try:
            task = TaskRecord.objects.get(pk=task_id)
        except TaskRecord.DoesNotExist:
            raise Http404("Task does not exist")

        form = ScheduleForm(initial={'schedule': task.schedule})
        return render(request, self.template_name, {'form': form, 'task': task})

    def post(self, request, task_id):
        try:
            task = TaskRecord.objects.get(pk=task_id)
        except TaskRecord.DoesNotExist:
            raise Http404("Task does not exist")

        form = ScheduleForm(request.POST)
        if form.is_valid():
            new_schedule = form.cleaned_data['schedule']

            if not is_valid_cron_expression(new_schedule):
                messages.error(request, 'Invalid cron expression. Please enter a valid cron schedule.')
                return render(request, self.template_name, {'form': form, 'task': task})

            try:
                croniter(new_schedule)
            except (ValueError, KeyError):
                messages.error(request, 'Invalid cron expression. Please enter a valid cron schedule.')
                return render(request, self.template_name, {'form': form, 'task': task})

            cron = CronTab(user=None)

            cron_command = f'python manage.py property_data {task_id}'

            existing_jobs = cron.find_comment(f'Scraping Task - {task_id}')
            for job in existing_jobs:
                cron.remove(job)

            job = cron.new(command=cron_command, comment=f'Scraping Task - {task_id}')
            job.setall(new_schedule)

            cron.write()

            return HttpResponseRedirect(reverse('admin:schedules_taskrecord_changelist'))

        return render(request, self.template_name, {'form': form, 'task': task})
