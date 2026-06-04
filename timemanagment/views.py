from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TimeTrackerSerializer, StatsSerializer
from .models import TimeTracker, TaskLog
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone



class TimeTrackerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        time_tracker = TimeTracker.objects.filter(user=request.user)
        serializer = TimeTrackerSerializer(time_tracker, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TimeTrackerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TimeTrackerDetailView(APIView): 
    
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, pk):
        obj = get_object_or_404(TimeTracker, pk=pk, user=request.user)
        serializer = TimeTrackerSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, pk):
        
        obj = get_object_or_404(TimeTracker, pk=pk, user=request.user)
        if 'dedicated_time' in request.data:
            time_to_add = request.data.get('dedicated_time', 0)
            today = timezone.localdate()
            
            
            log, created = TaskLog.objects.get_or_create(
                task=obj,
                date=today,
                defaults={'dedicated_time': 0}
            )
            
            log.dedicated_time += int(time_to_add)
            log.save()
     
        serializer = TimeTrackerSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(TimeTracker, pk=pk, user=request.user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
class StatView(APIView):
    permission_classes =[IsAuthenticated]
    
    def get(self, request, pk):
        task = get_object_or_404(TimeTracker, pk=pk, user=request.user)
        
        serializer = StatsSerializer(task, context = {'request': request})
        return Response(serializer.data)