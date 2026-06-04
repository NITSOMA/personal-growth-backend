from django.shortcuts import render
from .serializers import QuestionSerializer, JournalSerializer, JournalTemplateSerializer, JournalResponseSerializer
from .models import Question, JournalResponse, JournalTemplate, Journal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import datetime
from django.utils import timezone

class JournalTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
       
        templates = JournalTemplate.objects.filter(user=request.user, is_active=True)
        serializer = JournalTemplateSerializer(templates, many=True)
        return Response(serializer.data) 
        
    def post(self, request):
        serializer = JournalTemplateSerializer(data=request.data)
        if serializer.is_valid():
           
            serializer.save(user=request.user, is_default=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class JournalTemplateSingle(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, pk):
        template = get_object_or_404(JournalTemplate,  pk=pk, is_active=True)
        if template.user == request.user or template.is_default == True:
            serializer = JournalTemplateSerializer(template)
            return Response(serializer.data)
        return Response({"reposnse": "no data"})
    
    def delete(self, request, pk):  
        template = get_object_or_404(JournalTemplate, user=request.user, pk=pk, is_active=True)
        template.is_active = False
        template.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DefaultJournalTemplateView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        templates = JournalTemplate.objects.filter(is_default=True, is_active=True)
        serializer = JournalTemplateSerializer(templates, many=True)
        return Response(serializer.data)
    
    

class JournalView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        requested_date = request.query_params.get('date')
        
        
        if not requested_date:
            requested_date = timezone.localdate()
            
        
        journal = Journal.objects.filter(user=request.user, date=requested_date).first()
        
        if not journal:
            return Response(None) 
            
        serializer = JournalSerializer(journal)
        return Response(serializer.data)
    
    def post(self, request):
        
        serializer = JournalSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request):
        
        requested_date = request.query_params.get('date')
        if not requested_date:
            requested_date = timezone.localdate()
        obj = get_object_or_404(Journal, user=request.user, date=requested_date)
        serializer = JournalSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request):
        requested_date = request.query_params.get('date')
        if not requested_date:
            requested_date = timezone.localdate()
        obj = get_object_or_404(Journal, user=request.user, date=requested_date)
        obj.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)
        
        
            
    
    

        
class DatesView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        today = timezone.localdate()
        if not year:
            
           year = today.year
        if not month:
            month = today.month
        
        journals = Journal.objects.filter(
            user=request.user, 
            date__year=year,
            date__month=month
        ).values_list("date", flat=True)
        
        return Response(list(journals))
        
        
        
        