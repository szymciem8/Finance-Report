from django.shortcuts import render
from django.views import View

import pandas as pd
import yfinance as yf

import datetime

from django.contrib.auth.decorators import login_required

class FinanceReportView(View):

    # @login_required
    def get(self, request, stock='AAPL'):

        today = datetime.date.today().strftime('%Y-%m-%d')
        two_weeks_ago = (datetime.date.today() - datetime.timedelta(days=14)).strftime('%Y-%m-%d')

        df_yahoo = yf.download([stock], start=two_weeks_ago, end=today, progress=False)
        
        open_price = df_yahoo['Open'].values
        close_price = df_yahoo['Close'].values
        date = df_yahoo.index.values

        # Convert numpy datetime64 to datetime
        date = [pd.to_datetime(d).date().strftime('%Y-%m-%d') for d in date]

        context = {
            'stock': str(stock),
            'date': list(date),
            'open_price': list(open_price),
            'close_price': list(close_price)
        }

        return render(request, 'general_report_test.html', context=context)