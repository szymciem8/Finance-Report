from django.urls import path
from . import views

urlpatterns = [
    path('finance-report/', views.FinanceReportView.as_view(), name='register'),
]