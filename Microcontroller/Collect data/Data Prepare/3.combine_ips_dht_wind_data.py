import pandas as pd
import variables as v

def combine_date_time(df):
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)
    df = df.set_index('datetime')
    df = df.drop(columns=['Date', 'Time'])
    return df

door_df = pd.read_csv(f'{v.ips_door_path}')
window_df = pd.read_csv(f'{v.ips_window_path}')
center_df = pd.read_csv(f'{v.ips_center_path}')
dht22_df = pd.read_csv(f'{v.dht22_path}')
wind_df = pd.read_csv(f'{v.wind_path_out}')

door_df = combine_date_time(door_df)
window_df = combine_date_time(window_df)
center_df = combine_date_time(center_df)
dht22_df = combine_date_time(dht22_df)
wind_df = combine_date_time(wind_df)

door_df = door_df[~door_df.index.duplicated(keep='first')]
window_df = window_df[~window_df.index.duplicated(keep='first')]
center_df = center_df[~center_df.index.duplicated(keep='first')]
dht22_df = dht22_df[~dht22_df.index.duplicated(keep='first')]
wind_df = wind_df[~wind_df.index.duplicated(keep='first')]

min_timestamp = max(door_df.index.min(), window_df.index.min(), center_df.index.min(), dht22_df.index.min(), wind_df.index.min())
max_timestamp = min(door_df.index.max(), window_df.index.max(), center_df.index.max(), dht22_df.index.max(), wind_df.index.max())

door_df = door_df[(door_df.index >= min_timestamp) & (door_df.index <= max_timestamp)]
window_df = window_df[(window_df.index >= min_timestamp) & (window_df.index <= max_timestamp)]
center_df = center_df[(center_df.index >= min_timestamp) & (center_df.index <= max_timestamp)]
dht22_df = dht22_df[(dht22_df.index >= min_timestamp) & (dht22_df.index <= max_timestamp)]
wind_df = wind_df[(wind_df.index >= min_timestamp) & (wind_df.index <= max_timestamp)]

door_df = door_df.rename(columns=lambda col: f"{col}[door]")
window_df = window_df.rename(columns=lambda col: f"{col}[window]")
center_df = center_df.rename(columns=lambda col: f"{col}[center]")
dht22_df = dht22_df.rename(columns=lambda col: f"{col}[dht22]")

merged_df = pd.concat([center_df, window_df, door_df, dht22_df, wind_df], axis=1)

merged_df.to_csv(v.data_path_out)

print(f"""
      ==================================================================================
      Finished combining IPS files : {v.data_path_out}
      ==================================================================================
      """)