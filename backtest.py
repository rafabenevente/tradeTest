import csv
import os

import vectorbt as vbt
import pandas as pd

if __name__ == "__main__":
    # ticker names
    tickers = ["AAPL", "HD", "JNJ", "JPM", "MA", "NVDA"]
    headers = ["Strategy name", "End Value", "Total trades", "Best trade", "AVG win rate", "Worst trade", "AVG lose rate"]

    # read all files in stocks dir
    for file in tickers:
        # Create a folder to save images
        os.makedirs(f"backtest/{file}", exist_ok=True)

        data = pd.read_csv(f"stocks/{file}.csv")

        strategy = pd.read_csv(f"tests/df_data__{file}.csv")

        # convert close to a series object
        series = pd.Series(data["Close"])

        # set date as index
        series.index = data["Date"]

        # select the data greater than 01/01/2020
        series = series[series.index > "2020-01-01"]

        pf_hold = vbt.Portfolio.from_holding(series, init_cash=10000)
        fig = pf_hold.plot()
        fig.write_image(f"backtest/{file}/BuyAndHold.png")

        # select all columns with sufix "_REC"
        columns = [col for col in strategy.columns if col.endswith("_REC")]

        # open the file in the write mode
        f = open(f"backtest/{file}/{file}.csv", "w")

        # create the csv writer
        writer = csv.writer(f, delimiter=";")

        writer.writerow(headers)

        # Test all strategies
        for col in columns:
            # create a series with the entry points
            entries = pd.Series(strategy[col] == "buy")
            exits = pd.Series(strategy[col] == "sell")

            # create a backtest object
            pf = vbt.Portfolio.from_signals(series, entries, exits, init_cash=10000, fixed_fees=1, sl_stop=0.05, tp_stop=0.13)
            fig = pf.plot()
            fig.write_image(f"backtest/{file}/{col}.png")

            values = [col,
                      pf.final_value(),
                      pf.trades.count(),
                      pf.trades.returns.max() * 100,
                      pf.trades.winning.returns.mean() * 100,
                      pf.trades.returns.min() * 100,
                      pf.trades.losing.returns.mean() * 100]

            writer.writerow(values)

            # create a backtest for buy and hold

        values = ["Buy and hold",
                  pf_hold.final_value(),
                  pf_hold.trades.count(),
                  pf_hold.trades.returns.max() * 100,
                  pf_hold.trades.winning.returns.mean() * 100,
                  pf_hold.trades.returns.min() * 100,
                  pf_hold.trades.losing.returns.mean() * 100]
        writer.writerow(values)

        f.close()
