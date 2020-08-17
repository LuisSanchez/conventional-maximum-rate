from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from external_api import views

urlpatterns = [
    path('todayUF/', views.TodayUF.as_view()),
    path('tmcByYearAndMonth/<int:year>/<int:month>/', views.TMCByYearAndMonth.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
