import requests
import csv
import time
from datetime import datetime

# Replace with your ESP32 IP address
esp32_ip = "http://192.168.0.59/"

def get_sensor_data():
    try:
        temperature = requests.get(f"{esp32_ip}/temperature").text
        humidity = requests.get(f"{esp32_ip}/humidity").text
        return temperature, humidity
    except requests.RequestException as e:
        print("Error: ", e)
        return None, None

def save_to_csv(data, filename="sensor_data.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    # Header for CSV
    save_to_csv(["Timestamp", "Temperature (°C)", "Humidity (%)"])

    while True:
        current_time = datetime.now().time()
        if current_time >= datetime.strptime("07:00", "%H:%M").time() or current_time <= datetime.strptime("23:00", "%H:%M").time():
            temperature, humidity = get_sensor_data()
            if temperature and humidity:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                save_to_csv([timestamp, temperature, humidity])
                print(f"Data saved at {timestamp}")
            else:
                print("Failed to retrieve data.")
        else:
            print("Outside saving hours.")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
