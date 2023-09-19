from django.urls import path
from .views import ScrapeDataAPIView

urlpatterns = [
    path('scrape', ScrapeDataAPIView.as_view()),
]