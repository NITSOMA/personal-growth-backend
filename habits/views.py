from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from .models import Hebit, HebitLog
from .serializers import HebitSerializer, HebiTLogSerializer



class HebitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HebitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        habits = Hebit.objects.filter(user=request.user, is_active=True)
        serializer = HebitSerializer(habits, many=True)
        return Response(serializer.data)
    
    

    


class HebitDeleTeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        habit = get_object_or_404(Hebit, pk=pk, user=request.user)
        habit.is_active = False 
        habit.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    


class HabitLogCreate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        serializer = HebiTLogSerializer(data=request.data)
        if serializer.is_valid():
            habit = serializer.validated_data['habit']
            if habit.user != request.user:
                return Response(
                    {"error": "You do not own this habit."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HabitLogDelete(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, habit_id):
        today = timezone.localdate()
        log = get_object_or_404(
            HebitLog, 
            habit_id=habit_id,
            habit__user=request.user,
            date=today)
        log.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)
    
        





class HabitMonthGridView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        year_param = request.query_params.get('year')
        month_param = request.query_params.get('month')
        
        today = timezone.localdate()
        
       
        try:
            year_value = int(year_param) if year_param else today.year
            month_value = int(month_param) if month_param else today.month
            
            if not (1 <= month_value <= 12):
                raise ValueError("Month must be between 1 and 12.")
        except ValueError:
            return Response(
                {"error": "Invalid year or month format. Must be integers."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
       
        grid_data = HebitLog.objects.get_month_grid(
            user=request.user, 
            year_value=year_value, 
            month_value=month_value
        )
        
       
        return Response(grid_data, status=status.HTTP_200_OK)
    
    

        