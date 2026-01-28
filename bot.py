import yfinance as yf
import requests
import pandas as pd
from datetime import datetime

TOKEN = "8571388190:AAE_fyadym04D3MIrECC9tx_lExFmss_X1Q"
CHAT_ID = "6086785805"

ETFS = {
    "NIFTYBEES": "NIFTYBEES.NS",
    "SILVERBEES": "SILVERBEES.NS",
    "GOLDBEES": "GOLDBEES.NS",
    "HOLDINGS": "HDFCMFGETF.NS"
}

def RSI(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

final_msg = "📊 ETF MARKET UPDATE\n"
final_msg += f"🕒 {datetime.now().strftime('%d %b %Y | %I:%M %p')}\n\n"

for name, symbol in ETFS.items():
    data = yf.download(symbol, period="1y", interval="1d")

    close = data["Close"]
    rsi = RSI(close)
    ema200 = close.ewm(span=200).mean()

    price = float(close.iloc[-1])
    rsi_val = float(rsi.iloc[-1])
    ema_val = float(ema200.iloc[-1])

    if rsi_val < 40 and price > ema_val:
        signal = "🟢 STRONG BUY"
    elif rsi_val < 60:
        signal = "✅ BUY"
    elif rsi_val > 70:
        signal = "⚠️ PROFIT BOOK"
    else:
        signal = "⏳ HOLD"

    final_msg += f"""

    def predict_trend(price, ema200, rsi):
    score = 0

    if price > ema200:
        score += 40
    else:
        score -= 40

    if rsi < 40:
        score += 30
    elif rsi > 70:
        score -= 30

    if score >= 50:
        return "📈 Bullish", "High", f"{score}%"
    elif score >= 20:
        return "➡️ Sideways", "Medium", f"{score}%"
    else:
        return "📉 Bearish", "High", f"{score}%"
{name}
Price: ₹{round(price,2)}
RSI: {round(rsi_val,2)}
EMA200: {round(ema_val,2)}
Signal: {signal}

"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {"chat_id": CHAT_ID, "text": final_msg}
requests.post(url, data=payload)
