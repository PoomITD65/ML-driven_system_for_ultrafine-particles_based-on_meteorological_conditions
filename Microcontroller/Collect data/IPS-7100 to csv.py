import csv
import requests
import datetime
import time

url = 'http://192.168.0.170/sse'

def create_csv_filename():
    now = datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S")
    return f'Center_{now}.csv'

def write_csv_header(filename, headers):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

def write_to_csv(filename, data_values, user_values):
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")

    if len(data_values) < 28:
        print(f"Unexpected data format: {data_values}")
        return

    cleaned_data_values = [
        data_values[1].strip(),
        data_values[3].strip(),
        data_values[5].strip(),
        data_values[7].strip(),
        data_values[9].strip(),
        data_values[11].strip(),
        data_values[13].strip(),
        data_values[15].strip(),
        data_values[17].strip(),
        data_values[19].strip(),
        data_values[21].strip(),
        data_values[23].strip(),
        data_values[25].strip(),
        data_values[27].strip()
    ]

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, time_str] + cleaned_data_values + user_values)

def get_variable_input(prompt):
    while True:
        try:
            value = int(input(f"{prompt} (0: False, 1: True): "))
            if value in [0, 1]:
                return value
            else:
                print("Invalid input. Please enter 0 or 1.")
        except ValueError:
            print("Invalid input. Please enter a number (0 or 1).")

def main():
    print("Starting data collection...")

    headers = ["Date", "Time", "PC0.1", "PC0.3", "PC0.5", "PC1.0", "PC2.5", "PC5.0", "PC10", "PM0.1", "PM0.3", "PM0.5", "PM1.0", "PM2.5", "PM5.0", "PM10"]
    variables = ["Door", "Window 1 under air", "Window 2", "Fan 3", "Fan 5", "Steam sprayer", "Dehumidifier", "Air conditioner 25c"]
    user_values = []

    use_variables = input("Add variables? (y/n): ").strip().lower()
    if use_variables not in ['y', 'n']:
        print("Invalid input. Exiting the program.")
        return

    if use_variables == 'y':
        for var in variables:
            value = get_variable_input(var)
            user_values.append(value)
            headers.append(var)
    else:
        user_values = ["None"] * len(variables)
        headers.extend(variables)

    try:
        print('===============================================')
        incense_count = int(input("Number of incense sticks: "))
        headers.append("Incense Sticks")
        user_values.append(incense_count)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    try:
        print('===============================================')
        hours = int(input("Hours: "))
        minutes = int(input("Minutes: "))
        if hours < 0 or minutes < 0 or minutes >= 60:
            print("Minutes should be between 0 and 59.")
            return
    except ValueError:
        print("Invalid input.")
        return

    end_time = datetime.datetime.now() + datetime.timedelta(hours=hours, minutes=minutes)

    filename = create_csv_filename()
    write_csv_header(filename, headers)

    while datetime.datetime.now() < end_time:
        try:
            response = requests.get(url, stream=True, timeout=10)
            print("Connected to server, starting to receive data...")

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')

                    if "data:" in decoded_line:
                        data = decoded_line.split("data:")[1].strip()
                        data_values = data.split(",")

                        print(f"Received data: {data_values} (length: {len(data_values)})")

                        write_to_csv(filename, data_values, user_values)
                        print(data_values)

                        time.sleep(1)

                if datetime.datetime.now() >= end_time:
                    print("Stop data collection")
                    return

        except requests.exceptions.RequestException as e:
            print(f"Connection lost or failed, retrying... Error: {e}")
            time.sleep(5)

        except KeyboardInterrupt:
            print("Stopped by user")
            break

if __name__ == "__main__":
    main()
