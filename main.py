from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_trade = {
    "status": "WAITING",
    "type": None,
    "entry": 0.0,
    "tp": 0.0,
    "sl": 0.0
}

@app.get("/api/analysis-status")
def get_market_analysis():
    global active_trade
    
    # តម្លៃสำรอง (Fallback Price)
    current_price = 4260.00
    
    try:
        # ទាញយកតម្លៃ Spot មាសជាក់ស្តែងពី API ផ្ទាល់ (ស៊ីសង្វាក់គ្នាល្អជាមួយ OANDA)
        response = requests.get("https://api.gold-api.com/price/XAU", timeout=3)
        if response.status_code == 200:
            data = response.json()
            current_price = float(data.get("price", 4260.00))
    except Exception as e:
        print("មិនអាចទាញតម្លៃ API បានទេ:", e)

    # ស្ថានភាពរង់ចាំសញ្ញា (No Signal / Sideway)
    # ទីកន្លែងនេះអាចដាក់លក្ខខណ្ឌវិភាគបន្ថែមតាមតម្រូវការ
    signal_data = {
        "symbol": "XAUUSD",
        "action": "NO SIGNAL",
        "entry_price": round(current_price, 2),
        "rsi": 50.0,
        "stop_loss": 0,
        "tp1": 0, "tp2": 0, "tp3": 0,
        "logs": [
            {"time": "Now", "type": "SIDEWAY", "text": f"តម្លៃ Spot ជាក់ស្តែង: ${current_price:.2f} — ទីផ្សារ Sideway / រង់ចាំសញ្ញា"}
        ]
    }

    return {"success": True, "data": signal_data}