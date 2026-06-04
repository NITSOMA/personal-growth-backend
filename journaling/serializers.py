from rest_framework import serializers
from .models import Question, JournalTemplate, JournalResponse, Journal


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Question
        fields = ['id', 'text', 'order']
        
        

class JournalTemplateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    
    class Meta:
        model = JournalTemplate
        fields = ['id', 'name', 'is_public', 'questions', 'is_default']
        

    def create(self, validated_data):
        questions = validated_data.pop("questions")
        
        journal_template = JournalTemplate.objects.create(**validated_data)
        
        for question in questions:
            Question.objects.create(template=journal_template, **question)
        
        return journal_template
        

    
class JournalResponseSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    class Meta:
        model = JournalResponse
        fields = ['id', 'question', 'question_text', 'answer']
        
        
class JournalSerializer(serializers.ModelSerializer):
    responses = JournalResponseSerializer(many=True)
    
    class Meta:
        model = Journal
        fields = ['id', 'template_used', 'date', 'responses']
        
    def create(self, validated_data):
        responses_data = validated_data.pop('responses')
        journal = Journal.objects.create(**validated_data)
        
        for response_data in responses_data:
            JournalResponse.objects.create(journal=journal, **response_data)
            
        return journal
        
        

    
    
    
    

        