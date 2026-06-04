from django.urls import path
from .views import TimeTrackerView,  TimeTrackerDetailView, StatView


urlpatterns = [
    path("", TimeTrackerView.as_view()),
    path("<int:pk>/", TimeTrackerDetailView.as_view()),
    path("stats/<int:pk>/", StatView.as_view()),
]
