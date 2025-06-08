import yfinance as yf
import pandas as pd
from prophet import Prophet

def forecast_stock(symbol):
    df = yf.download(symbol, period="100d", interval="1d")
    
    if df.empty or "Close" not in df.columns:
        return None, f"No data found for {symbol}. Try another stock."

    df = df.reset_index()[['Date', 'Close']]
    df.columns = ['ds', 'y']

    if df['y'].isnull().all():
        return None, f"{symbol} does not have valid price data."

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=14)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat']], None
