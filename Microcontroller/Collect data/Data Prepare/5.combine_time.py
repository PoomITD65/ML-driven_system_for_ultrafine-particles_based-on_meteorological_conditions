import pandas as pd
import variables as v

to_combine1 = f'{v.finish_path_1}'
to_combine2 = f'{v.finish_path_2}'

output_file = f'{v.time_path_out}'

df1 = pd.read_csv(to_combine1)
df2 = pd.read_csv(to_combine2)

combined_df = pd.concat([df1, df2], ignore_index=True)

combined_df.to_csv(output_file, index=False)

print(f"""
      =========================================================================
      Combined data saved to {output_file} stick {v.stick2}
      =========================================================================
      """)
