import datetime
import matplotlib.pyplot as plt
import yfinance as yf

tt = yf.Ticker("FB")

for k in tt.info.keys():
    print(k)

print()
print(tt.info["shortName"])
print(tt.info["longName"])
print(tt.info["sector"])
print(tt.info["website"])
print(tt.info["longBusinessSummary"])
