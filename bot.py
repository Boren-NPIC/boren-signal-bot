import time
import requests
import os

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8541087672:AAGRli-wwUE_-cACSNMbdjnS7p916xU8EMQ")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7176722918")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending telegram: {e}")

def fetch_gold_price():
    # ប្រើប្រាស់ Public API ជំនួសដើម្បីទាញតម្លៃមាស (XAUUSD) ឱ្យបានត្រឹមត្រូវ
    try:
        # ប្រើប្រាស់ Metals-API ឬ Public endpoint ផ្សេង ឬ Free Forex/Gold API
        url = "https://data-asg.goldprice.org/dbXRates/USD"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        data = res.json()
        
        # យកតម្លៃមាសក្នុង ១ អង្សាឱន (Oz) ជា USD
        price = data['items'][0]['xauPrice']
        return float(price)
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def main_loop():
    print("🤖 Boren Signal Bot is running 24/7...")
    send_telegram_message("🚀 *BOREN-SIGNAL PRO* បានចាប់ផ្តើមដំណើរការលើ Cloud 24/7 ជោគជ័យ!")
    
    while True:
        price = fetch_gold_price()
        
        # ប្រសិនបើទាញតម្លៃមិនបាន ឬតម្លៃខុសប្រក្រតី (ឧទាហរណ៍ធ្លាក់ក្រោម 1000 ឬលើស 5000) អាចការពារទុកជាមុន
        if price and 1000 < price < 5000:
            print(f"Current Gold Price: ${price:.2f}")
            
            signal_type = "BUY" if price > 2000 else "SELL"
            entry = price
            
            if signal_type == "BUY":
                sl = price - 6
                tp = price + 12
            else:
                sl = price + 6
                tp = price - 12

            msg = f"🚨 *BOREN-SIGNAL PRO ELITE* 🚨\n🪙 XAUUSD - {signal_type}\n📥 Entry: ${entry:.2f}\n🛑 SL: ${sl:.2f}\n🎯 TP: ${tp:.2f}"
            send_telegram_message(msg)
            
            # សម្រាក 5 នាទីមុនផ្ញើរសារបន្ទាប់
            time.sleep(300)
        else:
            print("Fetching price failed or invalid price range, retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main_loop()