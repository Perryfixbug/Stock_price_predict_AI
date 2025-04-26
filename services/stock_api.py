import yfinance as yf

def get_stock_price(ticker_symbol: str):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period='1d', interval='1m')
    if data.empty:
        return None
    latest = data.iloc[-1]
    return {
        "price": round(latest['Close'], 2),
        "time": latest.name.strftime("%H:%M:%S")
    }

def get_historical_data(ticker_symbol: str, period: str = '1mo', interval: str = '1d'):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    data = data.reset_index()
    return data[['Date', 'Close']]  # hoặc thêm Volume, Open, v.v. nếu cần
