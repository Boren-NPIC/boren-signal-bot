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
    try:
        # ទាញតម្លៃមាស Spot ពីប្រភពទីផ្សារ
        url = "https://data-asg.goldprice.org/dbXRates/USD"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        data = res.json()
        price = data['items'][0]['xauPrice']
        return float(price)
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def main_loop():
    print("🤖 Boren Signal Bot with Trend Filter is running 24/7...")
    send_telegram_message("🚀 *BOREN-SIGNAL PRO (Trend Filter)* បានចាប់ផ្តើមដំណើរការលើ Cloud ជោគជ័យ!")
    
    # រក្សាទុកប្រវត្តិតម្លៃខ្លះៗដើម្បីយកมาคำนวณ Trend (Moving Average ងាយស្រួល)
    price_history = []

    while True:
        price = fetch_gold_price()
        
        if price and 1000 < price < 5000:
            print(f"Current Gold Price: ${price:.2f}")
            
            # បញ្ចូលតម្លៃថ្មីទៅក្នុងបញ្ជីប្រវត្តិ (រក្សាទុកត្រឹម 5 តម្លៃចុងក្រោយ)
            price_history.append(price)
            if len(price_history) > 5:
                price_history.pop(0)
            
            # ត្រូវមានទិន្នន័យគ្រប់គ្រាន់ទើបផ្ដើមវិភាគ Trend
            if len(price_history) == 5:
                # គណនាតម្លៃមធ្យម (Simple Moving Average) ខ្លីៗ
                sma = sum(price_history) / len(price_history)
                
                # Trend Filter Logic:
                # បើតម្លៃបច្ចុប្បន្នខ្ពស់กว่า SMA គឺ Bullish Trend (BUY)
                # បើទាបกว่า SMA គឺ Bearish Trend (SELL)
                if price > sma:
                    signal_type = "BUY"
                    entry = price
                    sl = price - 8.0   # ពង្រីកចម្ងាយ SL បន្តិចដើម្បីកុំឱ្យโดนសង្កត់កាត់លឿនពេក
                    tp = price + 15.0  # កំណត់ TP ឱ្យសមាមាត្រល្អ
                else:
                    signal_type = "SELL"
                    entry = price
                    sl = price + 8.0
                    tp = price - 15.0

                msg = (
                    f"🚨 *BOREN-SIGNAL PRO ELITE (Trend Filter)* 🚨\n"
                    f"🪙 XAUUSD - *{signal_type}*\n"
                    f"📈 Trend Status: {'BULLISH 🟢' if signal_type == 'BUY' else 'BEARISH 🔴'}\n"
                    f"📥 Entry: `${entry:.2f}`\n"
                    f"🛑 SL: `${sl:.2f}`\n"
                    f"🎯 TP: `${tp:.2f}`"
                )
                
                send_telegram_message(msg)
                print(f"Signal Sent: {signal_type} at ${entry:.2f}")
                
                # សម្រាករយៈពេល 10 នាទី (600 វិនាទី) មុននឹងចេញសញ្ញាបន្ទាប់ ដើម្បីធានាគុណភាព Signal
                time.sleep(600)
            else:
                time.sleep(60)
        else:
            print("Fetching price failed or invalid price range, retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main_loop()