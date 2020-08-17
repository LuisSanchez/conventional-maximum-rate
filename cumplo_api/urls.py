from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from cumplo_api import views

urlpatterns = [
    path('calculateTMC/', views.CalculateTMCForCredit.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
