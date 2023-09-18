from django.urls import path
from .views import ScheduleView  

urlpatterns = [
    path('schedule/<int:task_id>/', ScheduleView.as_view(), name='change_schedule'),  # Use as_view()

]
