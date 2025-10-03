import pandas as pd

try:
    df = pd.read_csv('weather_data.csv')

    print("Columns in the CSV file:")
    print(list(df.columns))

except FileNotFoundError:
    print("Error: The file was not found. Make sure the CSV is in the same folder.")