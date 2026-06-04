from django.urls import path
from .views import HebitView, HebitDeleTeView, HabitLogCreate, HabitLogDelete
from .views import HabitMonthGridView


urlpatterns = [
    path('', HebitView.as_view()),
    path('<int:pk>/', HebitDeleTeView.as_view()),
    path('logs/', HabitLogCreate.as_view()),
    path('logs/<int:habit_id>/', HabitLogDelete.as_view()),
  
    path("logs/grid/", HabitMonthGridView.as_view())
   
]
