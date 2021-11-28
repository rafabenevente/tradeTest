import vectorbt as vbt
import pandas as pd
import os

payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
first_table = payload[0]
symbols = first_table['Symbol'].values.tolist()
securities = first_table['Security'].values.tolist()

# create a datafrane to store the results
results = pd.DataFrame(columns=["Ticker","Name","Cross MA", "Hold", "Diference"])

INIT_CASH = 10000

for ticker, comp_name in zip(symbols, securities):
  # get data from ticker
  price = vbt.YFData.download(ticker.replace('.','-')).get('Close')

  # only data between 2020 and 2021
  price = price[price.index.year >= 2020]

  # calculate the MAs
  fast_ma = vbt.MA.run(price, 9, ewm=True)
  slow_ma = vbt.MA.run(price, 21)

  # calculate the cross MA
  entries = fast_ma.ma_above(slow_ma, crossover=True)
  exits = fast_ma.ma_below(slow_ma, crossover=True)

  # Do the backtest
  cros_ma = vbt.Portfolio.from_signals(price, entries, exits, init_cash=INIT_CASH)

  # Create a figure with the results
  fig = price.vbt.plot(trace_kwargs=dict(name='Price'))
  fig = fast_ma.ma.vbt.plot(trace_kwargs=dict(name='Fast MA'), fig=fig)
  fig = slow_ma.ma.vbt.plot(trace_kwargs=dict(name='Slow MA'), fig=fig)
  fig = entries.vbt.signals.plot_as_entry_markers(price, fig=fig)
  fig = exits.vbt.signals.plot_as_exit_markers(price, fig=fig)
  fig.write_image(f"moving_avg_test/{ticker}.png")

  # Do holding backtest
  hold = vbt.Portfolio.from_holding(price, init_cash=INIT_CASH)

  # Save results
  row = (ticker, 
         comp_name, 
         cros_ma.total_profit(), 
         hold.total_profit(), 
         cros_ma.total_profit() - hold.total_profit())
  results.loc[len(results)] = row

os.makedirs('moving_avg_test', exist_ok=True)
results.to_csv('moving_avg_test/best_tickers.csv')
