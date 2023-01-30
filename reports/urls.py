from django.urls import path
from . import views

urlpatterns = [
    path('add-finance-report/', views.AddFinanceReporView.as_view(), name='add_finance_report'),
    path('finance-report/', views.FinanceReportView.as_view(), name='register'),
    path('finance-report/<int:report_id>/', views.FinanceRerportDetailView.as_view(), name='finance_report_detail'),
    path('finance-report-list/', views.FinanceReportListView.as_view(), name='finance_report_list'),
    path('quick-report/', views.QuickReportView.as_view(), name='quick_report'),
]