import subprocess
import time

script_1 = "1.ane_to_csv_utf8.py"
script_2 = "2.combine_wind_speed.py"
script_3 = "3.combine_ips_dht_wind_data.py"
script_4 = "4.fill_missing_value.py"

scripts = [script_1, script_2, script_3, script_4]

cooldown = 1

for script in scripts:
    try:
        print(f"Running {script}...")
        subprocess.run(["python3", script], check=True)
        print(f"{script} executed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script}: {e}\n")

    if script != scripts[-1]:
        print(f"Waiting for {cooldown} seconds before running the next script...\n")
        time.sleep(cooldown)

print("All scripts executed.")