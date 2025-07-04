import pandas as pd
import variables as v

file_path = f'{v.data_path_out}'
data = pd.read_csv(file_path)

def fill_null_with_rolling_mean(series, window=3):
    return series.fillna(series.rolling(window=2*window+1, min_periods=1, center=True).mean())

data_filled = data.apply(lambda col: fill_null_with_rolling_mean(col) if col.dtype != 'object' else col)

output_path = f'{v.finish_path_out}'
data_filled.to_csv(output_path, index=False)

print(f"""
      ============================================================================================
      Finished filled null values using rolling mean : {output_path}
      ============================================================================================
      """)