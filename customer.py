import pandas as pd;
df = pd.read_csv(r"D:\Data analyst\Project py+s+e+powerbi\customer_shopping_behavior.csv")

print(df.head())
#Why r before the string?

#It makes the path a raw string, so backslashes (\) are treated correctly.
df.info()
#df.describe()

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.isnull().sum()

# Convert column names to lowercase
df.columns = df.columns.str.lower()

# Replace spaces with underscores
df.columns = df.columns.str.replace(' ', '_')

df=df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

#df.columns
print(df.columns)


#create a column age_group
labels = ['young Adult', 'Adult', 'Middle_aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)
print(df[['age', 'age_group']].head(10))


#create column purchase frequency days
frequency_mapping = {
    'Fortnightly' : 14,
    'Weekly' : 7,
    'Monthly' : 30,
    'Quarterly' : 90,
    'Bi-weekly' : 14,
    'Annually' : 365,
    'Every 3 months' : 90
}
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))

print(df[['discount_applied','promo_code_used']].head(10))

#its chcek its mapped correctly or not 

comparison = df['discount_applied'] == df['promo_code_used']
print(comparison.head())
print(comparison.all())

df = df.drop('promo_code_used',axis=1)
print(df.columns)








#Connect dataframe to workbench my sql
import pandas as pd
from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "Root"
host = "localhost"
port = "3306"
database = "customer_shopping"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# Write DataFrame to MySQL
table_name = "mytable"
df.to_sql(table_name, con=engine, if_exists="replace", index=False)

print("Data uploaded successfully!")

# Read first 5 rows from MySQL
query = pd.read_sql("SELECT * FROM mytable LIMIT 5;", con=engine)

print(query)

