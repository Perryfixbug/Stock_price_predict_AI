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

def get_info_data(ticker_symbol: str = "AAPL"):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    # Tính sự thay đổi (change) dựa trên giá đóng cửa hiện tại và giá đóng cửa trước đó
    previous_close = info.get("regularMarketPreviousClose", 0)
    current_price = info.get("currentPrice", 0)

    # Tính sự thay đổi theo phần trăm
    if previous_close > 0:
        change_percent = ((current_price - previous_close) / previous_close) * 100
    else:
        change_percent = 0

    return {
        "name": info.get("longName", "N/A"),
        "symbol": ticker_symbol,
        "price": round(current_price, 2),
        "change": round(change_percent, 2),
        "market_cap": info.get("marketCap", 0),
        "pe_ratio": info.get("forwardPE", 0),
        "dividend_yield": info.get("dividendYield", 0) * 100,
        "time": info.get("regularMarketTime", 0),
    }

def get_historical_data(ticker_symbol: str = 'AAPL', period: str = '1mo', interval: str = '1d'):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    data = data.reset_index()
    return data[['Date', 'Close', 'Open', 'High', 'Low', 'Volume']]  # hoặc thêm Volume, Open, v.v. nếu cần
