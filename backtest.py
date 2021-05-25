import talib
from zipline.api import order_target, record, symbol, order_target_percent


def initialize(context):

    stocklist = ["AMZN", "GOOGL", "MELI", "GLOB", "TSLA"]

    context.stocks = [symbol(s) for s in stocklist]

    context.target_pct_per_stock = 1.0 / len(context.stocks)

    context.LOW_RSI = 30
    context.HIGH_RSI = 70


def handle_data(context, data):
    # historical data
    prices = data.history(context.stocks, 'price',
                          bar_count=20, frequency='1d')

    rsis = {}
    # loop thrpugh stocks
    for stock in context.stocks:
        rsi = talib.RSI(prices[stock], timeperiod=14)[-1]  # prior day
        rsis[stock] = rsi
        current_position = context.portfolio.position[stock].amount
        # if RSI is over 70 and I am long

        if rsi > context.HIGH_RSI and current_position > 0 and data.can_trade(stock):
            order_target(stock, 0)
        elif rsi < context.LOW_RSI and current_position == 0 and data.can_trade(stock):
            order_target_percent(stock, context.target_pct_per_stock)


# record the current RSI val;ues of each stock
    record(amzn_rsi=rsis[symbol('AMZN')],
           googl_rsi=rsis[symbol('GOOGL')],
           meli_rsi=rsis[symbol('MELI')],
           glob_rsi=rsis[symbol('GLOB')],
           tsla_rsi=rsis[symbol('TSLA')])
