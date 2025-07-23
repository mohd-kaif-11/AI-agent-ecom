import pandas as pd
from sqlalchemy import create_engine

eligibility_df = pd.read_csv(r"C:\Users\kaif2\Desktop\ecom-qa-agent\data\Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv")
ad_sales_df = pd.read_csv(r"C:\Users\kaif2\Desktop\ecom-qa-agent\data\Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv")
total_sales_df = pd.read_csv(r"C:\Users\kaif2\Desktop\ecom-qa-agent\data\Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv")

engine = create_engine('sqlite:///ecommerce.db')

eligibility_df.to_sql('eligibility', engine, if_exists='replace', index=False)
ad_sales_df.to_sql('ad_sales_metrics', engine, if_exists='replace', index=False)
total_sales_df.to_sql('total_sales_metrics', engine, if_exists='replace', index=False)

print("Data loaded into ecommerce.db successfully!")
