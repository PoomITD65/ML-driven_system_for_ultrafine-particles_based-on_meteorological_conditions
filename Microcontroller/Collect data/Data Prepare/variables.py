# date
extension_csv = '.csv'
extension_ane = '.ane'

# day_date_main = '09-09-67'
# day_date_sub = '09.09'
# for_wind = '9.9'

# numberofstick = '15'

# # =================== input =================== #

# n_center = 'Center_09-09-2024_225233'
# n_dht = 'DHT22_09-09-2024_225341'
# n_door = 'Door_09-09-2024_225302'
# n_window = 'Window_09-09-2024_225332'
# --

day_of_ten = '28'
front_zero1 = ''

day_f = f'{front_zero1}{day_of_ten}'
day_ff  = f'{day_of_ten}'

month_of_ten = '9'
front_zero2 = '0'
month_f = f'{front_zero2}{month_of_ten}'
month_ff = f'{month_of_ten}'
year_th = '67'
year_en = '2024'

day_date_main = f'{day_f}-{month_f}-{year_th}'
day_date_sub = f'{day_f}.{month_f}'
for_wind = f'{day_f}.{month_ff}'
for_ips = f'{day_f}-{month_f}-{year_en}'

numberofstick = '5'

 # ================ all ====================== #

temppp =    '''''''''''''''''''''''''''''''''

                1 5 10 0

            '''''''''''''''''''''''''''''''''

stick1 = '1'
stick2 = '0'

finish_path_1 = f'data_combine/{day_date_sub}/{stick1}/!!Finish_data_{day_date_sub}.{stick1}{extension_csv}'
finish_path_2 = f'data_combine/{day_date_sub}/{stick2}/!!Finish_data_{day_date_sub}.{stick2}{extension_csv}'

finish_path_1 = f'data_combine/{day_date_sub}/combined_data_time.{day_date_sub}{extension_csv}'

time_path_out = f'data_combine/{day_date_sub}/combined_data_time.{day_date_sub}{extension_csv}'

# =================== input =================== #

n_center = f'Center_{for_ips}_{numberofstick}'
n_dht = f'DHT22_{for_ips}_{numberofstick}'
n_door = f'Door_{for_ips}_{numberofstick}'
n_window = f'Window_{for_ips}_{numberofstick}'

wind_door = f'door-backup-{for_wind}.{numberofstick}'
wind_window = f'window-backup-{for_wind}.{numberofstick}'

ips_door_path = f'{day_date_main}/{n_door}{extension_csv}'
ips_window_path = f'{day_date_main}/{n_window}{extension_csv}'
ips_center_path = f'{day_date_main}/{n_center}{extension_csv}'
dht22_path = f'{day_date_main}/{n_dht}{extension_csv}'

speed_wind_door = f'{day_date_main}/{day_date_sub}/{wind_door}{extension_ane}'
speed_wind_window = f'{day_date_main}/{day_date_sub}/{wind_window}{extension_ane}'

# ============================================= #

# =================== output =================== #

n_wind_door = '!door_wind_speed_'
n_wind_window = '!window_wind_speed_'

wind_door_path_out = f'data_combine/{day_date_sub}/{numberofstick}/{n_wind_door}{day_date_sub}.{numberofstick}{extension_csv}'
wind_window_path_out = f'data_combine/{day_date_sub}/{numberofstick}/{n_wind_window}{day_date_sub}.{numberofstick}{extension_csv}'

data_path_out = f'data_combine/{day_date_sub}/{numberofstick}/combine_data_{day_date_sub}.{numberofstick}{extension_csv}'
wind_path_out = f'data_combine/{day_date_sub}/{numberofstick}/combine_wind_{day_date_sub}.{numberofstick}{extension_csv}'
finish_path_out = f'data_combine/{day_date_sub}/{numberofstick}/!!Finish_data_{day_date_sub}.{numberofstick}{extension_csv}'
# ============================================== #