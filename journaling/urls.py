from django.urls import path
from .views import JournalTemplateView, JournalView, DatesView, JournalTemplateSingle, DefaultJournalTemplateView

urlpatterns = [
    path('templates/', JournalTemplateView.as_view()),
    path('templates/<int:pk>/', JournalTemplateSingle.as_view()),
    path('templates/defaults/', DefaultJournalTemplateView.as_view()),
    path('journals/', JournalView.as_view()),
    
    path('dates/', DatesView.as_view()),
]


