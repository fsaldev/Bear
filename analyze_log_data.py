import pandas as pd

# Assuming you have the necessary data and have already executed the code to read and process the CSV file
df = pd.read_csv('logs_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Grouping the data by date and counting occurrences
df_grouped = df.groupby('Date')['Date'].count().reset_index(name='Count')

# Specifying the Excel file name (change 'output_file.xlsx' to your desired file name)
excel_file_name = 'output_file.xlsx'

# Exporting the grouped data to Excel
df_grouped.to_excel(excel_file_name, index=False)

# Printing the grouped data
print(df_grouped)
print(f'Data has been exported to {excel_file_name}')
