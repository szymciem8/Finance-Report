from celery import shared_task
from datetime import datetime
from time import sleep


from .report_templates.stock_report import FinanceReportPDF


@shared_task
def generate_report(stock):
    now = datetime.now().strftime('%Y-%m-%d')
    path = f'documents/{stock}-{now}.pdf'
    try:
        FinanceReportPDF(path, stock)
    except:
        sleep(3)
        generate_report(stock)