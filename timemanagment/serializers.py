from rest_framework import serializers
from .models import TimeTracker
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta



class TimeTrackerSerializer(serializers.ModelSerializer):
    time_today = serializers.SerializerMethodField()
    
    
    class Meta:
        model = TimeTracker
        fields = ['id', 'name', 'time_today']
        
    def get_time_today(self, obj):
        today = timezone.localdate()
        log = obj.logs.filter(date=today).first()
        return log.dedicated_time if log else 0
    
    
    
    
    
class StatsSerializer(serializers.ModelSerializer):
    total_time = serializers.SerializerMethodField()
    
    
    class Meta:
        model = TimeTracker
        fields = ['id', 'name', 'total_time']
    
    
    
    def get_total_time(self, obj):
        request = self.context.get('request')
        days = 0
        if request and "days" in request.query_params:
            try:
                days = int(request.query_params.get("days"))
            except ValueError:
                pass
        if days == 0:
            total = obj.logs.aggregate(Sum('dedicated_time'))['dedicated_time__sum']
            
        else:
            start_date = timezone.localdate() - timedelta(days=days)
            total = obj.logs.filter(date__gte=start_date).aggregate(Sum('dedicated_time'))['dedicated_time__sum']
            
        return total or 0