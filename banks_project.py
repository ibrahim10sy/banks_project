import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
from sqlalchemy import create_engine

#  CONFIGURATION 
log_file = "code_log.txt"
csv_path = 'Largest_banks_data.csv'
output_path = "banks_data.csv"
table_name = 'Largest_banks'
url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attributs = ['Name','MC_USD_Billion']
table_target = ['Name','MC_USD_Billion','MC_GBP_Billion','MC_EUR_Billion','MC_INR_Billion']

# CONNEXION MYSQL
engine = create_engine("mysql+pymysql://root:AtmLaRNEC59ypgUCukf3@localhost/banksdb",  future=True)


# log
def log_progress(message):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(message + ',' + timestamp + '\n')

# extraction 
def extract(url, table_attributs):
    df = pd.DataFrame(columns=table_attributs)
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
    
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {
                'Name': col[0].get_text(strip=True),
                'MC_USD_Billion': col[2].get_text(strip=True)
            }
            df1 = pd.DataFrame([data_dict])
            df = pd.concat([df, df1], ignore_index=True)

    return df

# transformation 
def transform(data, csv_path):
    exchange_rate = {
        'GBP': 0.8,
        'EUR': 0.93,
        'INR': 82.95
    }

    data['MC_USD_Billion'] = pd.to_numeric(data['MC_USD_Billion'], errors='coerce')

    data['MC_GBP_Billion'] = [round(x * exchange_rate['GBP'], 2) if pd.notna(x) else np.nan for x in data['MC_USD_Billion']]
    data['MC_EUR_Billion'] = [round(x * exchange_rate['EUR'], 2) if pd.notna(x) else np.nan for x in data['MC_USD_Billion']]
    data['MC_INR_Billion'] = [round(x * exchange_rate['INR'], 2) if pd.notna(x) else np.nan for x in data['MC_USD_Billion']]

    data.to_csv(csv_path, index=False)
    return data

# exportation csv 
def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)

# chargement dans la base de donnée
def load_to_db(df, engine, table_name):
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

# requeête sql
def run_query(query_statement, engine):
    print(f"Exécution de : {query_statement}")
    result = pd.read_sql(query_statement, engine)
    print(result)

# ---------- ETL PROCESSUS ----------

log_progress("ETL Job Started")

# 1. Extraction
log_progress("Extract phase Started")
extracted_data = extract(url, table_attributs)
print("Données extraites :\n", extracted_data.head())
log_progress("Extract phase Ended")

# 2. Transformation
log_progress("Transform phase Started")
transformed_data = transform(extracted_data, csv_path)
print("Données transformées :\n", transformed_data.head())
log_progress("Transform phase Ended")

# 3. Chargement dans CSV
log_progress("Load phase Started")
load_to_csv(transformed_data, output_path)
log_progress("Load phase Ended")

# 4. Chargement dans MySQL
log_progress("MySQL DB Load Started")
load_to_db(transformed_data, engine, table_name)
log_progress("MySQL DB Load Ended")

# 5. Requêtes SQL
log_progress("SQL Query Started")
run_query(f"SELECT * FROM {table_name} LIMIT 5", engine)
run_query(f"SELECT AVG(MC_GBP_Billion) as Moyenne_GBP FROM {table_name}", engine)
run_query(f"SELECT Name FROM {table_name} ORDER BY MC_USD_Billion DESC LIMIT 5", engine)
log_progress("SQL Query Ended")

log_progress("ETL Job Ended")
