import requests
import pandas as pd
from datetime import datetime
import time


def get_exchange_rates_yahoo(
    from_currency: str = "IDR",
    to_currency: str = "GBP",
    start_date: str = "2017-01-01",
) -> pd.DataFrame:
    """
    Fetch historical exchange rates from Yahoo Finance.
    Completely free, no API key, supports IDR and all major currencies.
    Returns daily OHLC data — we use the closing rate.
    """
    ticker = f"{from_currency.upper()}{to_currency.upper()}=X"

    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_ts   = int(datetime.now().timestamp())

    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?interval=1d&period1={start_ts}&period2={end_ts}"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }

    print(f"Fetching {from_currency}/{to_currency} from Yahoo Finance...")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    # Navigate the Yahoo Finance response structure
    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    closes     = result["indicators"]["quote"][0]["close"]

    rows = []
    for ts, close in zip(timestamps, closes):
        if close is not None:
            rows.append({
                "Date": pd.to_datetime(ts, unit="s").normalize(),
                "Rate": close,
                "From": from_currency.upper(),
                "To":   to_currency.upper(),
            })

    df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)
    return df


df = get_exchange_rates_yahoo("IDR", "GBP", start_date="2017-01-01")
print(df)
print(f"\nTotal rows : {len(df)}")
print(f"Date range : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"Rate range : {df['Rate'].min():.8f} → {df['Rate'].max():.8f}")
