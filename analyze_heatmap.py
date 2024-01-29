import pandas as pd


df = pd.read_csv("heat_maps.csv")
daily_sum = df.groupby("Day")["Times"].sum().reset_index()
total_sum = df["Times"].sum()
print("Sum of Times for Each Day:")
print(daily_sum)

print("\nTotal Sum of Times:")
print(total_sum)
