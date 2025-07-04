import csv
import pandas as pd
from datetime import datetime
import variables as v

def convert_ane_to_csv(input_file, output_file):

    with open(input_file, 'r', encoding='ISO-8859-1') as ane_file:
        data = ane_file.readlines()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        for line in data:
            row = line.strip().split(',')

            try:
                date = datetime.strptime(row[0], '%Y-%m-%d').strftime('%d/%m/%Y')
                row[0] = date
            except ValueError:
                pass
            writer.writerow(row)
    
    df = pd.read_csv(output_file)
    
    if 'Unnamed: 5' in df.columns:
        df = df.drop(columns=['Unnamed: 5'])
    
    df.to_csv(output_file, index=False)

pathin_window = f'{v.speed_wind_window}'
pathout_window = f'{v.wind_window_path_out}'

pathin_door = f'{v.speed_wind_door}'
pathout_door = f'{v.wind_door_path_out}'

convert_ane_to_csv(pathin_window, pathout_window)
convert_ane_to_csv(pathin_door, pathout_door)

print(f"""
      ==================================================================================
      Finished converting ane files to CSV file : {pathout_window}
      Finished converting ane files to CSV file : {pathout_door}
      ==================================================================================
      """)