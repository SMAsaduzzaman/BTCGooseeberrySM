import MetaTrader5 as mt5

def place_sell_order(tp, deviation=20):
    symbol = "BTCUSD"
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol {symbol}.")
        return None

    tick_info = mt5.symbol_info_tick(symbol)
    if tick_info is None:
        print(f"Could not retrieve tick info for symbol {symbol}.")
        return None

    price = tick_info.bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.01,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        'tp': tp,
        "sl": 0.0,
        "deviation": deviation,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: {result.retcode if result else 'None'}")
        if result is not None:
            print("Order result details:", result)
        return None
    return result
