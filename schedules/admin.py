from django.contrib import admin
from .models import TaskRecord
from django.urls import reverse
from .cron import run_command
from django.http import HttpResponseRedirect


@admin.register(TaskRecord)
class ScrapingTaskRecordAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'records_scraped', 'status')
    list_filter = ('status', 'enabled') 
    actions = ['enable_tasks', 'disable_tasks', 'trigger_tasks']

    def enable_tasks(self, request, queryset):
        queryset.update(status='pending')

    enable_tasks.short_description = 'Enable selected tasks'

    def disable_tasks(self, request, queryset):
        queryset.update(status='completed')

    disable_tasks.short_description = 'Disable selected tasks'

    def trigger_tasks(self, request, queryset):
        
        for task in queryset:
            if task.enabled:
                run_command(task.id)
        return HttpResponseRedirect(reverse('admin:your_app_scrapingtaskrecord_changelist'))

    trigger_tasks.short_description = 'Trigger selected tasks'
