from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, db  # ใช้ db (Realtime Database)
from datetime import datetime

# =============================================
# ✅ 1. เชื่อมต่อ Firebase Realtime Database
# =============================================

cred = credentials.Certificate(r"D:/!---Final_Project_Walailak---!/Code/MY_WEB/Path/web-application-predictionpm01-firebase.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://web-application-predictionpm01-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

realtime_db = db.reference("/")  # ใช้ reference ไปที่ root ของ Realtime Database

# =============================================
# ✅ 2. สร้าง FastAPI instance และกำหนด CORS
# =============================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================
# ✅ 3. API ดึงค่า Standard Deviation (SD) ล่าสุด
# =============================================

@app.get("/sd_pm_data_1m")
async def get_sd_pm_data_1m():
    """
    ดึงค่า Standard Deviation (SD) ล่าสุดจาก Realtime Database (SD_1min)
    """
    sd_data = realtime_db.child("SAC/SD_1min").get()

    if not sd_data:
        return {"error": "No SD data found"}

    return {
        "PM25_SD": sd_data.get("PM25_SD", "N/A"),
        "PM01_SD": sd_data.get("PM01_SD", "N/A"),
        "Temperature_SD": sd_data.get("Temperature_SD", "N/A"),
        "Humidity_SD": sd_data.get("Humidity_SD", "N/A")
    }

# =============================================
# ✅ 4. API ดึงข้อมูลเฉลี่ย 1 นาทีล่าสุด
# =============================================

@app.get("/average_pm_data_1m")
async def get_average_pm_data_1m():
    """
    ดึงข้อมูลเฉลี่ย 1 นาทีล่าสุดจาก Realtime Database (data_averaged_1m)
    """
    avg_data = realtime_db.child("data_averaged_1m").order_by_key().limit_to_last(1).get()

    if not avg_data:
        return {"error": "No 1-minute average data found"}

    avg_data = list(avg_data.values())[0]

    return {
        "pm2_5": avg_data.get("pm2_5", "N/A"),
        "temperature": avg_data.get("temperature", "N/A"),
        "humidity": avg_data.get("humidity", "N/A"),
        "pm0_1_predicted": avg_data.get("pm0_1_predicted", "N/A")
    }

# =============================================
# ✅ 5. API ดึงข้อมูลเฉลี่ย 1 ชั่วโมงล่าสุด
# =============================================

@app.get("/average_pm_data_1h")
async def get_average_pm_data_1h():
    """
    ดึงข้อมูลเฉลี่ย 1 ชั่วโมงล่าสุดจาก Realtime Database (data_averaged_1h)
    """
    avg_data = realtime_db.child("data_averaged_1h").order_by_key().limit_to_last(1).get()

    if not avg_data:
        return {"error": "No 1-hour average data found"}

    avg_data = list(avg_data.values())[0] if isinstance(avg_data, dict) else {}

    return {
        "pm2_5": avg_data.get("pm2_5", "N/A"),
        "temperature": avg_data.get("temperature", "N/A"),
        "humidity": avg_data.get("humidity", "N/A"),
        "pm0_1_predicted": avg_data.get("pm0_1_predicted", "N/A")
    }

# =============================================
# ✅ 6. API ดึงข้อมูลเฉลี่ย 24 ชั่วโมงล่าสุด
# =============================================

@app.get("/average_pm_data_24h")
async def get_average_pm_data_24h():
    avg_data = realtime_db.child("data_averaged_24h").order_by_key().limit_to_last(1).get()

    if not avg_data:
        return {"error": "No 24-hour average data found"}

    avg_data = list(avg_data.values())[0]

    return {
        "pm2_5": avg_data.get("pm2_5", "N/A"),
        "temperature": avg_data.get("temperature", "N/A"),
        "humidity": avg_data.get("humidity", "N/A"),
        "pm0_1_predicted": avg_data.get("pm0_1_predicted", "N/A")
    }

