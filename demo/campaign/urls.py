""" views importation"""
from django.urls import path
from .views import (
    ScrapeDataAPIView,
    TaskStatusAPIView,
    GetLinkedInData,
    GenerateEmailAPI,
    GenerateEmailsAPI,
)


urlpatterns = [
    path('scrape', ScrapeDataAPIView.as_view()),
    path('scrape/<str:task_id>', TaskStatusAPIView.as_view()),
    path("linkedin", GetLinkedInData.as_view()),
    path("email", GenerateEmailAPI.as_view()), 
    path("email_generator", GenerateEmailsAPI.as_view()),
]