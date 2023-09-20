from django.urls import path
from .views import (ScrapeDataAPIView, PromptAPIView)

urlpatterns = [
    path('scrape', ScrapeDataAPIView.as_view()),
    path('prompt', PromptAPIView.as_view()),
]