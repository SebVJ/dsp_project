import pandas as pd

df = pd.read_excel('/Users/andreasbrogaard/Documents/dsp_project/EDC w. description.xlsx')

print(df['Description'].iloc[1])