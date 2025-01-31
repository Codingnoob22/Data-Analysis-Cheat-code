import pandas as pd
import chardet 
import seaborn as sns
import matplotlib.pyplot as plt

#CHECKING THE DATA
#load the data
df = pd.read_csv('super_store.csv', encoding='ISO-8859-1')

#Showing column
print(df.columns)

#CLEANING THE DATA
#Drop Duplicates
clean_dupe = df.drop_duplicates(subset='Order ID', keep='first')

#Clean negative values
no_negative = df[df['Quantity'] > 0]

#Remove N/A data
total_revenue = df['Sales'].fillna(0).sum()
print(f"Total Revenue: ${total_revenue:,.2f}")


#Advanced
#Replace missing revenue with the median (skewed distributions)
df['Sales'] = df['Sales'].fillna(df['Sales'].median())
advanced_revenue = df['Sales']
total_revenue_advanced = advanced_revenue.fillna(0).sum()
print(f"Total Revenue Advanced: ${total_revenue_advanced:,.2f}")

#Replace N/A values with Unknown
df['Customer ID'] = df['Customer ID'].fillna('Unknown')
advanced_technique = df['Customer ID']
print(f"advanced_technique")


#BUSINESS APPROACH
#Grouping n aggregation sales based on region
sales_summary = df.groupby(['Region', 'Category'])['Profit'].agg(['sum', 'mean'])
print(sales_summary)

print("-------------------------------")
#Compare sales at each region
pivot_table = df.pivot_table(
    index='Region',
    columns='Category',
    values='Sales',
    aggfunc='sum',
    fill_value=0
)
print(pivot_table)

#Categorize consument into each segment, from high to low 
bins = [0, 100, 500, float('inf')]
labels = ['Low', 'Medium', 'High']
df['spending_segment'] = pd.cut(df['Sales'], bins=bins, labels=labels)
sorted_htol = df.sort_values(by='spending_segment', ascending=False)
print(sorted_htol)


#Calculating monthly revenue
df['Order Date'] = pd.to_datetime(df['Order Date'])
monthly_revenue = df.resample('ME', on='Order Date')['Sales'].sum()
print(monthly_revenue)

#Calculating Quarterly revenue
df['Order Date'] = pd.to_datetime(df['Order Date'])
quarterly_revenue = df.resample('QE', on='Order Date')['Sales'].sum()
print(quarterly_revenue)

#Convert from Series to Dataframe
quarterly_revenue = quarterly_revenue.reset_index()

#Rename columns for clarity
quarterly_revenue.columns = ['Sales', 'Profit']

#Calculate quarter-over-quarter (QoQ) growth
quarterly_revenue['Quarterly Growth'] = quarterly_revenue['Profit'].pct_change()
print(quarterly_revenue)

#Convert it as percentage
quarterly_revenue['Quarterly Growth %'] = quarterly_revenue['Quarterly Growth'].apply(lambda x: f"{x:.2%}" if pd.notnull(x) else '')
print(quarterly_revenue)

#Plot the growth
plt.figure(figsize=(8, 5))
plt.plot(quarterly_revenue['Sales'], quarterly_revenue['Profit'], marker='o')
plt.title('Quarter-over-Quarter Revenue Growth')
plt.xlabel('Quarter')
plt.ylabel('QoQ Growth')
plt.grid(True)
plt.show()