import numpy as np
from pandas import *

from datetime import datetime

import matplotlib.finance as fin
import numpy as np
from pylab import show


from pandas import Index, DataMatrix
from pandas.core.datetools import BMonthEnd

#-------------------------------------------------------------------------------
# Demo data set from Yahoo finance

startDate = datetime(2000, 1, 1)
endDate = datetime(2010, 1, 1)

def getQuotes(symbol, start, end):
    quotes = fin.quotes_historical_yahoo(symbol, start, end)
    dates, open, close, high, low, volume = zip(*quotes)

    data = {
        'open' : open,
        'close' : close,
        'high' : high,
        'low' : low,
        'volume' : volume
    }

    dates = Index([datetime.fromordinal(int(d)) for d in dates])
    return DataMatrix(data, index=dates)

def get_etf_panel():
    data = {}
    for symbol in _etfs:
        print symbol
        data[symbol] = getQuotes(symbol, startDate, endDate)

    return WidePanel.fromDict(data, intersect=False)

def get_stock_panel():
    data = {}
    for symbol in _tickers:
        print symbol
        data[symbol] = getQuotes(symbol, startDate, endDate)

    return WidePanel.fromDict(data, intersect=False)

_etfs = ['BND','DBC','GLD','IWC','JNK','MUB','PCY','TIP','VB','VGK',
         'VNQ','VO','VPL','VV','VWO','WPS', 'SPY', 'TBT', 'TLT']

_stocks = ['AAPL', 'MSFT', 'GOOG', 'YHOO']

_tickers = ['AGCO', 'DE']

#-------------------------------------------------------------------------------
# Demo

wp = WidePanel.load('examples/etf_data')

wp.items
wp.major_axis
wp.minor_axis

wp = wp.swapaxes('items', 'minor')
dm = wp['close']
tlt = dm['TLT']

dm.mean()
dm.std()
dm.std(1)

# plot the dispersion

s = tlt[-5:]
s2 = s.asfreq("WEEKDAY")

# fine
s + s2

dm.reindex(columns=['BND', 'GLD', 'TIP', 'TLT']).plot()


# structured arrays

arr = np.ones(10, dtype=[('A', 'f8'), ('B', 'f8'),
                         ('C', 'f8'), ('D', 'f8')])
# arr['A'] = np.arange(10)


# But all is not lost
dm = DataMatrix.fromRecords(arr)

lp = wp.toLong()
lp2 = lp.truncate(before=datetime(2009, 12, 25))

arr = lp.toRecords()

dm = pivot(arr['major'], arr['minor'], arr['close'])

# regression

close = wp['close']
returns = close / close.shift(1) - 1

y_var = 'GLD'
x_vars = ['SPY', 'TIP', 'BND', 'JNK']

all = x_vars + [y_var]
model = ols(y=returns[y_var], x=returns.reindex(columns=x_vars))
correl = returns.reindex(columns=all).corr()

ts_model = ols(y=returns[y_var], x=returns.reindex(columns=x_vars),
               window_type='rolling', window=131)
