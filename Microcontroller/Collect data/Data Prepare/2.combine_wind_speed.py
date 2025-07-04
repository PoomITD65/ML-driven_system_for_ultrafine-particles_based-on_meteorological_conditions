import pandas as pd
import variables as v

door_df = pd.read_csv(f'{v.wind_door_path_out}')
window_df = pd.read_csv(f'{v.wind_window_path_out}')

door_data = door_df.iloc[:, [0, 1, 2]]
window_data = window_df.iloc[:, [0, 1, 2]]

door_data.columns = ['Date', 'Time', 'door_wind_speed']
window_data.columns = ['Date', 'Time', 'window_wind_speed']

combined_df = pd.merge(door_data, window_data, on=['Date', 'Time'], how='inner')

output_path = f'{v.wind_path_out}'
combined_df.to_csv(output_path, index=False)

print(f"""
      ==================================================================================
      Finished combining wind speed files :{output_path}
      ==================================================================================
      """)