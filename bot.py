import yfinance as yf
import requests
import json
import os

TOKEN = os.getenv("8571388190:AAE_fyadym04D3MIrECC9tx_lExFmss_X1Q")
CHAT_ID = os.getenv("6086785805")

ETF = "NIFTYBEES.NS"
STATE_FILE = "last_signal.json"

def get_signal():
    data = yf.download(ETF, period="6mo", interval="5m")
    close = data["Close"]

    rsi = 100 - (100 / (1 + (close.diff().clip(lower=0).rolling(14).mean() /
                              close.diff().clip(upper=0).abs().rolling(14).mean())))

    ema = close.ewm(span=200).mean()

    price = close.iloc[-1]
    rsi_val = rsi.iloc[-1]
    ema_val = ema.iloc[-1]

    if rsi_val < 40 and price > ema_val:
        return "BUY"
    elif rsi_val > 70:
        return "SELL"
    else:
        return "HOLD"

def get_last_signal():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)["signal"]
    return None

def save_signal(signal):
    with open(STATE_FILE, "w") as f:
        json.dump({"signal": signal}, f)

signal = get_signal()
last_signal = get_last_signal()

if signal != last_signal:
    msg = f"📢 ETF SIGNAL ALERT\n\nETF: NIFTYBEES\nSignal: {signal}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    save_signal(signal)
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
