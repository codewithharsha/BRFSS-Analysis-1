import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sys
df = pd.read_csv("weather_data.csv")

# Database connection settings
host = "localhost"
port = "5432"
dbname = "BRFSS_Data"
user = "postgres"
password = "2002"
table_name = "weather_data"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

# Create table & insert data
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data loaded into table '{table_name}' in database '{dbname}'")

