import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sys
df = pd.read_csv(sys.argv[1])

# Database connection settings
host = "host.docker.internal"
port = "5432"
dbname = "BRFSS_Data"
user = "postgres"
password = "2002"
table_name = "brfss_data"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

# Create table & insert data
df.to_sql(table_name, engine, if_exists='append', index=False)

print(f"Data loaded into table '{table_name}' in database '{dbname}'")

print("No.of rows inserted from the chunk are:",len(df))
