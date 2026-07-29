import time
import requests
import os

# Telegram Configuration (យក Token និង Chat ID របស់អ្នកមកដាក់ទីនេះ ឬដាក់ក្នុង Environment Variables)
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
    # ប្រើប្រាស់ Public API ដើម្បីទាញតម្លៃមាស ឬ Crypto មកវិភាគ
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        data = res.json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def main_loop():
    print("🤖 Boren Signal Bot is running 24/7...")
    send_telegram_message("🚀 *BOREN-SIGNAL PRO* បានចាប់ផ្តើមដំណើរការលើ Cloud 24/7 ជោគជ័យ!")
    
    while True:
        price = fetch_gold_price()
        if price:
            print(f"Current Gold Price: ${price}")
            
            # លក្ខខណ្ឌសាកល្បង (អាចប្តូរជាកូដវិភាគបច្ចេកទេសផ្សេងទៀតតាមតម្រូវការ)
            if price % 5 == 0:  
                signal_type = "BUY" if price > 2000 else "SELL"
                
                # កែតម្រូវ Logic គណនា SL និង TP ឱ្យត្រូវតាមប្រភេទ Signal
                if signal_type == "BUY":
                    entry = price
                    sl = price - 6    # BUY: SL ត្រូវនៅខាងក្រោមតម្លៃ Entry
                    tp = price + 12   # BUY: TP ត្រូវនៅខាងលើតម្លៃ Entry
                else:
                    entry = price
                    sl = price + 6    # SELL: SL ត្រូវនៅខាងលើតម្លៃ Entry
                    tp = price - 12   # SELL: TP ត្រូវនៅខាងក្រោមតម្លៃ Entry

                msg = f"🚨 *BOREN-SIGNAL PRO ELITE* 🚨\n🪙 XAUUSD - {signal_type}\n📥 Entry: ${entry}\n🛑 SL: ${sl}\n🎯 TP: ${tp}"
                send_telegram_message(msg)
                
        # រង់ចាំ 60 វិនាទី មុនពេលឆ្កឹះតម្លៃម្តងទៀត (ការពារជាប់ Rate Limit)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()