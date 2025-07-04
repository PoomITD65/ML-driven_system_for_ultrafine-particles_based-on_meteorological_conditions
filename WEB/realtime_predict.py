import os
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# 🔹 กำหนด Full Path ของโมเดลและ Firebase Credentials
MODEL_PATH = r"D:/!---Final_Project_Walailak---!/Code/MY_WEB/Model/LightGBM_model_save3.pkl"
FIREBASE_CREDENTIALS_PATH = r"D:/!---Final_Project_Walailak---!/Code/MY_WEB/Path/web-application-predictionpm01-firebase.json"

# 🔹 ตรวจสอบไฟล์ก่อนโหลด
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file not found at: {MODEL_PATH}")

if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    raise FileNotFoundError(f"❌ Firebase credentials not found at: {FIREBASE_CREDENTIALS_PATH}")

# 🔹 โหลดโมเดล
with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)
print("🔥 Model Loaded Successfully!")

# 🔹 เชื่อมต่อ Firebase Realtime Database
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://web-application-predictionpm01-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
print("🔥 Firebase Connected Successfully!")

def predict_pm0_1(pm2_5, temperature, humidity, wind_speed):
    """
    ✅ ใช้โมเดลพยากรณ์ค่า PM0.1
    """
    features = np.array([pm2_5, temperature, humidity, wind_speed]).reshape(1, -1)
    predicted_pm0_1 = model.predict(features)[0]
    return round(predicted_pm0_1, 4)

def process_data(data, storage_path, avg_storage_path):
    """
    ✅ ใช้ค่าที่ได้รับจาก Sensor ใน Firebase
    ✅ พยากรณ์ค่า PM0.1
    ✅ บันทึก `datetime` และ `pm0_1_predicted` ไปยัง `storage_path`
    ✅ รวมข้อมูลและบันทึกลง `avg_storage_path` **(ไม่รวม wind_speed และ datetime)**
    """
    pm2_5 = data.get("PM25")
    temperature = data.get("Temperature")
    humidity = data.get("Humidity")
    wind_speed = data.get("Windspeed")
    datetime = data.get("Timestamp")  # ใช้เป็น key เท่านั้น

    # 🔹 Debug: ตรวจสอบค่าที่ได้รับ
    print("----------------------------------------------------------")
    print(f"🔍 Received Data: PM2.5={pm2_5}, Temperature={temperature}, Humidity={humidity}, Wind Speed={wind_speed}, Timestamp={datetime}")

    # 🔹 ถ้ามีค่าขาดหาย ให้ข้ามไป
    if None in [pm2_5, temperature, humidity, wind_speed, datetime]:
        print("❌ Missing sensor data! Skipping prediction...")
        return

    # 🔹 พยากรณ์ค่า PM0.1
    predicted_pm0_1 = predict_pm0_1(pm2_5, temperature, humidity, wind_speed)
    print(f"🔥 Prediction: PM0.1 = {predicted_pm0_1} mg/m³")

    # 🔹 บันทึกค่าพยากรณ์ลง `storage_path`
    pred_ref = db.reference(storage_path)
    pred_ref.child(datetime).set({
        "pm0_1_predicted": predicted_pm0_1
    })

    print(f"✅ Prediction stored successfully in `{storage_path}`!")

    # 🔹 รวมค่าพยากรณ์กับข้อมูลเซ็นเซอร์ **โดยไม่รวม wind_speed และ datetime**
    result = {
        "pm2_5": pm2_5,
        "temperature": temperature,
        "humidity": humidity,
        "pm0_1_predicted": predicted_pm0_1  # ✅ ค่าทำนาย
    }

    # 🔹 บันทึกค่าที่รวมแล้วลง `avg_storage_path`
    avg_ref = db.reference(avg_storage_path)
    avg_ref.child(datetime).set(result)  # ✅ ใช้ datetime เป็น key แต่ไม่เก็บใน JSON

    print(f"✅ Averaged data stored successfully in `{avg_storage_path}`!")
    print("----------------------------------------------------------")
    print("⏳ Waiting for new data...")
    print("----------------------------------------------------------")

def on_data_change_min(event):
    print("----------------------------------------------------------")
    print("📡 New data detected in MicroClimate_1min!")
    if isinstance(event.data, dict):
        process_data(event.data, "data_predicted", "data_averaged_1m")
    else:
        print("❌ Error: Received non-dictionary data! Skipping...")
        print("----------------------------------------------------------")

def on_data_change_hour(event):
    print("----------------------------------------------------------")
    print("📡 New data detected in MicroClimate_1hour!")
    if isinstance(event.data, dict):
        process_data(event.data, "data_predicted_1h", "data_averaged_1h")
    else:
        print("❌ Error: Received non-dictionary data! Skipping...")
        print("----------------------------------------------------------")

def on_data_change_day(event):
    print("----------------------------------------------------------")
    print("📡 New data detected in MicroClimate_1day!")
    print("----------------------------------------------------------")
    if isinstance(event.data, dict):
        process_data(event.data, "data_predicted_24h", "data_averaged_24h")
    else:
        print("❌ Error: Received non-dictionary data! Skipping...")
        print("----------------------------------------------------------")

ref_min = db.reference("SAC/MicroClimate_1min/227_C3/Point01")
ref_min.listen(on_data_change_min)

ref_hour = db.reference("SAC/MicroClimate_1hour/227_C3/Point01")
ref_hour.listen(on_data_change_hour)

ref_day = db.reference("SAC/MicroClimate_1day/227_C3/Point01")
ref_day.listen(on_data_change_day)

print("⏳ Waiting for new data...")