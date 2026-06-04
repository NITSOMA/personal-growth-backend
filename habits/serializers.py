from .models import Hebit, HebitLog
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Hebit, HebitLog
from django.utils import timezone


class HebitSerializer(ModelSerializer):
    
    completed_today = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Hebit
        fields =['id', 'name', 'user', 'completed_today']
        
        read_only_fields = ['user', 'completed_today']
        
        
    def validate_name(self, value):
        correct_spacing = " ".join(value.split())
        name_cleaned = correct_spacing.capitalize()
        return name_cleaned
    
    def get_completed_today(self, obj):
        
        today = timezone.localdate()
        return HebitLog.objects.filter(habit=obj, date=today).exists()
        
        

    
    
        
class HebiTLogSerializer(serializers.ModelSerializer):
    habit_name = serializers.SerializerMethodField()
    class Meta:
        model = HebitLog
        fields =["habit", "habit_name", "date"]
    def get_habit_name(self, obj):
        return obj.habit.name
        
 
        
        
    
