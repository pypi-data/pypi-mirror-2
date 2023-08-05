from pandas import *
wp = WidePanel.load('examples/etf_data')
wp
wp.items
wp.major_axis
wp.major_axis[0]
wp.minor_axis
wp.items
wp.items.indexMap
'BND' in wp.items
wp.items[5:10]
wp.items[5:10].indexMap
wp['BND']
dm = wp['BND']
dm['close']
s = dm['close']
type(s)
s.plot()
s.index
s2 = s[-5:]
s2 * 2
s2.mean()
s2.std()
s3 = s2.asfreq('WEEKDAY')
s2 + s3
s3 = s2.asfreq('WEEKDAY', fillMethod='pad')
s3 p= s2.asfreq('WEEKDAY')
s3 = s2.asfreq('WEEKDAY')
s2 + s3
s3 = s2.asfreq('WEEKDAY', fillMethod='pad')
s3 = s2.asfreq('WEEKDAY')
s3 = s2.asfreq('WEEKDAY', fillMethod='pad')
s3 = s2.asfreq('WEEKDAY', fillMethod='backfill')
s3 = s2.asfreq('WEEKDAY')
s3.fill(0)
dm = wp['BND']
dm[-5:]
dm[-5:].asfreq('WEEKDAY')
dm2 = dm[-5:].asfreq('WEEKDAY')
dm2
dm2.dropEmptyRows()
dm2.dropIncompleteRows()
dm2

dm2
dm2['close'] = 0
dm2
dm2.dropIncompleteRows(['close'])

wp = WidePanel.load('examples/etf_data')
wp
wp
wp = wp.swapaxes('items', 'minor')
ep
wp
close = wp['close']
close
close.getXS(datetime(2009, 12, 31))
s = close.getXS(datetime(2009, 12, 31))
s
close
dm[-5:]
close[-5:]
close[-5:].T
dm2 = close[-5:].T
dm2
dm2.mean()
dm2.mean(axis=1)
dm2 = dm2.copy()
dm2
dm['VPL'] = NaN
dm
dm2['VPL'] = NaN
dm2
dm2.mean()
dm2 = close[-5:].T
dm2
dm2.values
dm2.columns
dm2.index
dm2.values
dm2
wp
wp
means = wp.mean('major')
means
counts = wp.count('items')
counts
wp
wp.count('minor')
wp.count('minor')['close']
figure()
wp.count('minor')['close'].plot()
dm
wp
dm = wp['close']
dm
dm
dm.mean()
dm.std()
dm.skew()
dm.apply(np.std)
dm.apply(np.sqrt)
dm.apply(np.log)
dm2 = close[-5:].T
dm2
dm2[datetime(2010, 1, 1)] = 1
dm2
del dm2[datetime(2010, 1, 1)]
dm2
dm2 * 2
wp
close = wp['close']
close
returns = close / close.shift(1) - 1
returns
vols = rolling_std(returns, 250, min_periods=100)
vols = rolling_std(returns, 250, minPeriods=100)
vols
vols['GLD'].plot()
figure()
vols['GLD'].plot()
returns
rolling_corr(returns['GLD'], returns['TIP'])
rolling_corr(returns['GLD'], returns['TIP'], 250)
rolling_corr(returns['GLD'], returns['TIP'], 250)
figure()
rolling_corr(returns['GLD'], returns['TIP'], 250).plot()
rolling_corr(returns['GLD'], returns['TIP'], 250)
returns.apply(lambda x: rolling_std(x, 261))
returns.apply(lambda x: rolling_std(x, 261))
returns['BND']
ts = returns['BND']
ts2 = ts[-5:]
ts2.asfreq(datetools.Minute(), fillMethod='pad')
dm.reindex(columns=['BND', 'GLD', 'TIP', 'TLT'])
dm.reindex(columns=['BND', 'GLD', 'TIP', 'TLT'])
rets = returns.reindex(columns=['BND', 'GLD', 'TIP', 'TLT'])
rets[-5:]
dm = rets[-5:]
dm + dm[:2]
dm
rets
rets.corr()
rets.plot()
figure()
rets.plot()
rets.cumprod().plot()
figure()
(1 + rets).cumprod().plot()
legend()
rets
rets * 1
rets + rets['BND']
rets - returns['SPY']
rets.mean(1)
rets.mean(0)
rets
y_var = 'GLD'
x_vars = ['SPY', 'TIP', 'BND', 'JNK']

all = x_vars + [y_var]
model = ols(y=returns[y_var], x=returns.reindex(columns=x_vars))
model
model.t_stat
model.beta
model.r2
ts_model = ols(y=returns[y_var], x=returns.reindex(columns=x_vars),
               window_type='rolling', window=131)
ts_model
figure()
model.beta
ts_model.beta
model.beta.plot()
figure()
ts_model.beta.plot()
legend(loc='best')
figure()
ts_model.t_stat.plot()
legend(loc='best')
type(ts_model)
ts_model
ts_model.summary_as_matrix
ts_model
arr = np.ones(10, dtype=[('A', 'f8'), ('B', 'f8'),
                         ('C', 'f8'), ('D', 'f8')])
DataMatrix.fromRecords(arr)
dm.shift(1)
dm.shift(1) + dm
dm.shift(1)
dm.shift(1) + dm
lp = wp.truncate(before=datetime(2009, 12, 25)).toLong()
lp = wp.reindex(wp.major_axis[-5:])).toLong()
lp = wp.reindex(wp.major_axis[-5:]).toLong()
lp
lp.toString()
lp.toRecords()
lp.toRecords()
lp.toRecords()
