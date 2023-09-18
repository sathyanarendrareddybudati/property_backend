from djongo import models

class Property(models.Model):
    
    property_name = models.CharField(max_length=255)
    property_cost = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255)
    property_area = models.CharField(max_length=255)
    property_locality = models.CharField(max_length=255)
    property_city = models.CharField(max_length=255)
    individual_property_link = models.URLField()

class TaskRecord(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    records_scraped = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    schedule = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f'Task Record {self.pk}'