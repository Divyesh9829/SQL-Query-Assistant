import sqlite3
import pandas as pd
import os

# Define the path to your CSV/XLSX directory and the database file
data_dir = 'data/csv_xlsx'
db_path = 'data/csv_xlsx_sqldb.db'

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to import CSV files
def import_csv(file_name):
    try:
        csv_file_path = os.path.join(data_dir, file_name)
        table_name = os.path.splitext(file_name)[0]
        df = pd.read_csv(csv_file_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Imported {file_name} into {table_name} table")
    except Exception as e:
        print(f"Error importing {file_name}: {e}")

# Function to import Excel files
def import_excel(file_name):
    try:
        excel_file_path = os.path.join(data_dir, file_name)
        xls = pd.ExcelFile(excel_file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df.to_sql(sheet_name, conn, if_exists='replace', index=False)
            print(f"Imported {file_name} sheet {sheet_name} into {sheet_name} table")
    except Exception as e:
        print(f"Error importing {file_name}: {e}")

# Loop through files in the data directory and import them
for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        import_csv(file)
    elif file.endswith('.xlsx') or file.endswith('.xls'):
        import_excel(file)

# Commit changes and close the connection
conn.commit()
conn.close()
