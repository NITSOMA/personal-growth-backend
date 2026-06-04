from django.db import models
from django.conf import settings
from django.utils import timezone


class JournalTemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Question(models.Model):
    template = models.ForeignKey(JournalTemplate, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=350)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
class Journal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template_used = models.ForeignKey(JournalTemplate, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.localdate)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_daily_journal')
        ]
    
    
class JournalResponse(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.TextField()