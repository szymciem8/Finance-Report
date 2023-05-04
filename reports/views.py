from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

import yfinance as yf

from .models import FinanceReport
from .utils import generate_finance_report
from .tasks import generate_report


VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

class AddFinanceReporView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'add_finance_report.html')

    @csrf_exempt
    def post(self, request):
        report_name = request.POST.get('report-name')
        stock = request.POST.get('stock').upper()
        period = request.POST.get('period')

        # Checing if stock exists
        if not yf.Ticker(stock).info:
            return render(request, 'add_finance_report.html', {'error_message': 'Stock does not exist'})

        if period not in VALID_PERIODS:
            return render(request, 'add_finance_report.html', {'error_message': 'Invalid period'})

        report = FinanceReport.objects.create(user=request.user, name=report_name, stock=stock, period=period)

        # Assign Report to User
        user = request.user
        user.finance_reports.add(report)

        report_id = report.id

        return redirect('/reports/finance-report/{}/'.format(report_id))


class FinanceRerportDetailView(LoginRequiredMixin, View):

    def get(self, request, report_id):
        report = FinanceReport.objects.get(id=report_id)

        # Check if user is owner of report
        if request.user != report.user:
            return render(request, 'finance_report_detail.html', {'error_message': 'You do not own this report'})

        stock = report.stock
        period = report.period

        context = generate_finance_report(stock, period)

        return render(request, 'general_report_test.html', context=context)


class FinanceReportListView(LoginRequiredMixin, View):

    def get(self, request):
        reports = FinanceReport.objects.filter(user=request.user).order_by('-creation_date')
        reports = reports.values()
        username = request.user.username

        context = {
            'reports': reports,
            'username': username
        }
        return render(request, 'finance_report_list.html', context=context)


class QuickReportView(View):

    def get(self, request, stock='AAPL', period='1mo'):
        stock = stock.upper()
        period = period.lower()

        if period not in VALID_PERIODS:
            return render(request, 'general_report_test.html', {'error_message': 'Invalid period'})

        context = generate_finance_report(stock, period)

        return render(request, 'quick_finance_report.html', context=context)

    @csrf_exempt
    def post(self, request):
        stock = request.POST.get('stock').upper()
        period = request.POST.get('period').lower()

        if period not in VALID_PERIODS:
            return render(request, 'general_report_test.html', {'error_message': 'Invalid period'})

        context = generate_finance_report(stock, period)

        return render(request, 'quick_finance_report.html', context=context)

class FinanceReportView(View):

    def get(self, request, stock='AAPL', period='1mo'):
        stock = request.GET.get('stock', 'AAPL').upper()
        period = request.GET.get('period', '1mo')
        
        context = generate_finance_report(stock, period)

        return render(request, 'general_report_test.html', context=context)
    

class FinanceReportPDFView(APIView):
    
    def get(self, request):

        stock = request.GET.get('stock').upper()

        generate_report.delay(stock)
        return Response({'message':'Starting report generation process'})
