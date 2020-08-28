from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from external_api import views

urlpatterns = [
    path('todayUF/', views.TodayUF.as_view(), name="todayUF"),
    path('tmcByYearAndMonth/<int:year>/<int:month>/', views.TMCByYearAndMonth.as_view(), name="tmc"),
    path('utmByYearAndMonth/<int:year>/<int:month>/', views.UTMByYearAndMonth.as_view(), name="utm"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
