import yfinance as yf

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.piecharts import Pie

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import Color


def money_converter(amount):
    if abs(amount) >= 1_000_000_000_000:
        return f"${amount / 1_000_000_000_000:.2f} T"
    elif abs(amount) >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f} B"
    elif abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:.2f} M"
    else:
        return f"${amount:.2f}"


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width, self.height = LETTER

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if (self._pageNumber > 1):
                self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        # self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Times-Roman', 10)
        self.drawString(LETTER[0]-x, 65, page)
        self.restoreState()


class FinanceReportPDF:

    def __init__(self, path, stock):
        self.path = path
        self.stock = stock
        self.ticker = yf.Ticker(stock)
        self.styles = getSampleStyleSheet()
        self.ticker_info = self.ticker.info
        self.title = f'{stock} Report'
        self.elements = []
        self.title = Paragraph(f"<h1>{self.title}</h1>", self.styles["Heading1"])

        self.green = Color((45.0/255), (166.0/255), (153.0/255), 1)
        self.elements.extend([self.title])

        # Pages
        self.first_page()
        self.holders_page()
        self.history_page()

        self.doc = SimpleDocTemplate(path, pagesize=A4)
        self.doc.multiBuild(self.elements, canvasmaker=FooterCanvas)


    def first_page(self):
        summary = self.ticker_info.get('longBusinessSummary', None)
        self.elements.append(Paragraph(f"<h2>Stock summary</h2>", self.styles["Heading2"]))
        info = Paragraph(f"<p> {summary} </p>")
        self.elements.extend([info, Spacer(1, 0.5*inch)])
        self.create_stock_info_table()
        self.elements.append(PageBreak())

    def holders_page(self):
        self.create_holders_tables()
        self.elements.append(PageBreak())

    def holders_pie_page(self):
        self.create_pie_chart()
        self.elements.append(PageBreak())

    def history_page(self):
        style = [('VALIGN',(0,0),(-1,-1),'CENTER'), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),]
        self.elements.append(Paragraph(f"<h2>Stock history</h2>", self.styles["Heading2"]))

        self.create_titles(('1 Month', '3 Months'))

        d1 = self.create_history_chart(period='1mo', width=200, x_drawing=200)
        d2 = self.create_history_chart(period='3mo', width=180, x_drawing=180)
        
        data = [(d1, d2)]
        t = Table(data)
        t.setStyle(TableStyle(style))
        self.elements.append(t)

        self.elements.append(Spacer(1, 0.1*inch))
        self.create_titles(('6 Months'))

        drawing = self.create_history_chart(period='6mo')
        self.elements.extend([drawing])

        self.elements.append(Spacer(1, 0.1*inch))
        self.create_titles(('1 Year'))
        drawing = self.create_history_chart(period='1y')
        self.elements.extend([drawing])

        self.elements.append(PageBreak())


    def create_titles(self, titles):
        title_style = [('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
                       ('FONTSIZE', (0, 0), (-1, -1), 14),
                       ]

        t = Table([titles], colWidths=[3*inch]*len(titles))
        t.setStyle(TableStyle(title_style))
        self.elements.append(t)

    def create_stock_info_table(self):

        table_style = [('BACKGROUND', (0, 1), (0, 0), colors.grey),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white)]

        keys = ['marketCap', 'dividendRate', 'dividendYield', 'totalRevenue', 'revenuePerShare', 'totalDebt',
                'debtToEquity', 'returnOnAssets', 'returnOnEquity', 'grossProfits', 'freeCashflow' 'operatingCashflow',
                'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins', 'auditRisk', 
                'boardRisk', 'beta', 'trailingPE', 'forwardPE', 'volume', 'regularMarketVolume',
                ]

        data = self.gather_info_data(keys)
        data1 = data[:len(data)//2]
        data2 = data[len(data)//2:]

        t1 = Table(data1)
        t1.setStyle(TableStyle(table_style))

        t2 = Table(data2)
        t2.setStyle(TableStyle(table_style))

        data = [(t1, t2)]
        t = Table(data)
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),]))
        self.elements.append(t)


    def gather_info_data(self, keys):
        data = []
        for key in keys:
            value = self.ticker_info.get(key, None)
            if value:
                value = money_converter(value)
                data.append([key, value])
        return data
    

    def create_holders_tables(self):
        table_style = [('BACKGROUND', (0, 1), (0, 0), colors.grey),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white)]

        self.elements.append(Paragraph(f"<h2>Institutional Holders</h2>", self.styles["Heading2"]))

        values, labels = self.gather_pie_chart_data('institutional')
        data = self.gather_holders_info('institutional')
        t2 = Table(data)
        t2.setStyle(TableStyle(table_style))
        self.elements.append(t2)
        self.elements.append(Spacer(1, 0.25*inch))
        self.create_pie_chart(values, labels, label_radius=2)

        self.elements.append(PageBreak())

        self.elements.append(Paragraph(f"<h2>Mutualfund Holders</h2>", self.styles["Heading2"]))
        values, labels = self.gather_pie_chart_data('mutualfund')
        data = self.gather_holders_info('mutualfund')
        t1 = Table(data)
        t1.setStyle(TableStyle(table_style))
        self.elements.append(t1)

        self.create_pie_chart(values, labels, label_radius=2)


    def gather_pie_chart_data(self, type='mutalfund'):
        if type == 'mutualfund':
            df = self.ticker.mutualfund_holders
        elif type == 'institutional':
            df = self.ticker.institutional_holders

        return df['Value'].values.tolist(), df['Holder'].values.tolist()
    

    def gather_holders_info(self, type='mutalfund'):
        if type == 'mutualfund':
            df = self.ticker.mutualfund_holders
        elif type == 'institutional':
            df = self.ticker.institutional_holders

        df['Shares'] = df['Shares'].apply(lambda x: money_converter(x))
        df['Value'] = df['Value'].apply(lambda x: money_converter(x))
        df['% Out'] = df['% Out'].apply(lambda x: f'${x:.3f}')
        df['Date Reported'] = df['Date Reported'].apply(lambda x: str(x)[:-9])

        data = [df.columns.values]
        data.extend(df.values.tolist())

        return data


    def create_history_chart(self, height=100, width=450, x_drawing=500, y_drawing=120, period='1mo'):
        open = self.ticker.history(period=period)['Open'].values
        close = self.ticker.history(period=period)['Close'].values
        data = [open, close]

        # Create a container for the chart
        drawing = Drawing(x_drawing, y_drawing)

        lc = HorizontalLineChart()
        lc.x = 10
        lc.y = 10
        lc.height = height
        lc.width = width
        lc.data = data
        lc.joinedLines = 1
        # catNames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
        # lc.categoryAxis.categoryNames = catNames
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.valueAxis.valueMin = min(open)-10
        lc.valueAxis.valueMax = max(open)+10
        lc.valueAxis.valueStep = 15
        lc.lines[0].strokeWidth = 2
        lc.lines[1].strokeWidth = 1.5
        drawing.add(lc)

        return drawing


    def create_pie_chart(self, data, labels, label_radius=1.5):
        drawing = Drawing(600, 290)

        pc = Pie()
        pc.x = 140
        pc.y = 0
        pc.width = 150
        pc.height = 150
        pc.data = data
        pc.labels = labels

        pc.simpleLabels = 0
        pc.slices.strokeWidth=0.5
        pc.slices.labelRadius = label_radius
        pc.slices.label_simple_pointer = 1
        pc.slices.label_boxAnchor = 's'
        pc.slices.popout = 5
        drawing.add(pc)

        self.elements.extend([drawing, Spacer(1, 0.1*inch)])