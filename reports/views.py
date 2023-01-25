from django.shortcuts import render

# Create your views here.
def finance_report(request):
    return render(request, 'finance_report.html')