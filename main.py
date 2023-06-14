import pandas as pd
import re

sales_data = pd.read_csv("sales_data.csv")

sales_data["Year"] = pd.to_datetime(sales_data["Date"]).dt.year
sales_data["Month"] = pd.to_datetime(sales_data["Date"]).dt.month.astype(str).str.zfill(2)
sales_data["Category"] = sales_data["Notes"].str.extract

sales_data = sales_data.dropna()

sales_data["Product"] = sales_data["Product"].str.strip()
sales_data["Quantity"] = sales_data["Quantity"].astype(int)
sales_data["Category"] = sales_data["Notes"].str.extract(r'\[(.*)\]').fillna('')
sales_data["Notes"] = sales_data["Notes"].apply(lambda x: re.sub(r'\W+', ' ', x)).astype(str).str.lstrip(' ')

sales_data.to_csv("new_sales_data.csv", index = False)

sales_data["Revenue"] = sales_data["Quantity"] * sales_data["Price"]

analyze = pd.DataFrame(sales_data.groupby("Product").agg({"Revenue": 'sum', "Quantity": 'sum'})).reset_index()
analyze["Average Price per Unit"] = round(analyze["Revenue"] / analyze["Quantity"], 2)

print("The product with the highest total sales revenue is: " + analyze["Product"].loc[analyze["Revenue"].idxmax()])

analyze = analyze.rename(columns = {"Revenue": "Total Sales Revenue", "Quantity": "Total Quantity Sold"})
analyze.to_csv("sales_summary.csv", index = False)
