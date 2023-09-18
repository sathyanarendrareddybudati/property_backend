from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import TaskRecord
from .forms import ScheduleForm
from crontab import CronTab
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

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

            cron = CronTab(user=None)

            cron_command = f'python manage.py property_data {task_id}'

            existing_jobs = cron.find_comment(f'Scraping Task - {task_id}')
            for job in existing_jobs:
                cron.remove(job)

            job = cron.new(command=cron_command, comment=f'Scraping Task - {task_id}')
            job.setall(new_schedule)

            cron.write()

            return HttpResponseRedirect(reverse('admin:your_app_scrapingtaskrecord_changelist'))

        return render(request, self.template_name, {'form': form, 'task': task})
