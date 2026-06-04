from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
import calendar

from datetime import date


class HabitLogQuerySet(models.QuerySet):
    
    def _get_base_qs(self, user, filter_kwargs):
        return self.filter(habit__user=user, **filter_kwargs)

    def get_month_grid(self, user, year_value, month_value):
        
        year_value = int(year_value)
        month_value = int(month_value)
        

        _, total_days = calendar.monthrange(year_value, month_value)
        
      
        logs = self._get_base_qs(user, {
            'date__year': year_value, 
            'date__month': month_value
        }).values('date').annotate(completed_count=Count('id'))
        
     
        logs_map = {log['date'].day: log['completed_count'] for log in logs}
        
        grid_data = []
        
       
        for day in range(1, total_days + 1):
            current_date = date(year_value, month_value, day)
            
           
            total_active_habits_that_day = user.habits.filter(
                start_date__lte=current_date
            ).filter(
                models.Q(deactivated_at__isnull=True) | models.Q(deactivated_at__gt=current_date)
            ).count()
            
            actual_completions = logs_map.get(day, 0)
            
       
            percentage = 0.0
            if total_active_habits_that_day > 0:
                percentage = round((actual_completions / total_active_habits_that_day) * 100, 1)

            grid_data.append({
                "date": current_date.isoformat(),
                "day": day,
                "total_completed": actual_completions,
                "total_active_habits": total_active_habits_that_day,
                "percentage": percentage
            })
            
        return grid_data



    

        

class Hebit(models.Model):
    name = models.CharField(max_length=112)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    deactivated_at = models.DateField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], 
                condition=models.Q(is_active=True),
                name='unique_active_user_habit'
            )
        ]
        
    def __str__(self):
        return self.name
    

    


class HebitLog(models.Model):
    habit = models.ForeignKey(Hebit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.now)
   
    
    objects = HabitLogQuerySet.as_manager()
    
    
    class Meta:
        unique_together = ('habit', 'date')
        
        
    def __str__(self):
        return f"{self.habit.name} done {self.date}"
