from django.db import models
from django.conf import settings
from django.utils import timezone


class TimeTracker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=132)
   
    
    
    class Meta:
       
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_task')
        ]
        
    
    
class TaskLog(models.Model):
    task = models.ForeignKey(TimeTracker, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.localdate)
    dedicated_time = models.IntegerField(default=0)
    
    
    class Meta:
        
        constraints = [
            models.UniqueConstraint(fields=['task', 'date'], name='unique_task_date')
        ]
