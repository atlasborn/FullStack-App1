import pandas as pd
import os
import sqlite3
import json

def quantity_sells_by_day(df) -> pd.DataFrame:
    df_copy = df.copy()
    sells = df_copy.groupby(df_copy['InvoiceDate'].dt.date)['Quantity'].sum().reset_index(name='QuantitySum')
    return sells

def profit_per_day(df) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy['InvoiceDate']= pd.to_datetime(df_copy['InvoiceDate'], errors= 'coerce')
    df_copy['Profit'] = df_copy['Quantity'] * df_copy['UnitPrice']
    sells = df_copy.groupby(df_copy['InvoiceDate'].dt.date)['Profit'].sum().reset_index(name='Profit')
    return sells

def sells_per_category(df) -> pd.DataFrame:
    df_copy = df.copy()
    sells = df_copy.groupby(df_copy['Description'])['Quantity'].sum().reset_index(name='QuantitySum')
    return sells.sort_values(by='QuantitySum', ascending=False)

def profit_at_categories(df) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy['UnitPrice'] = pd.to_numeric(df_copy['UnitPrice'])
    df_copy['Quantity'] = pd.to_numeric(df_copy['Quantity'])
    df_copy['Profit'] = df_copy['UnitPrice']  * df_copy['Quantity']
    sells = df_copy.groupby(df_copy['Description'])['Profit'].sum().reset_index(name='Profit')
    sells.sort_values(by='Profit', ascending=False, inplace=True)
    return sells

df = pd.read_csv('data/raw/data.csv', encoding='latin-1', sep=',')
df.dropna()
df['InvoiceDate']= pd.to_datetime(df['InvoiceDate'], errors= 'coerce')

json_output = {
        'profit_days': profit_per_day(df).to_json(),
        'profit_categories': profit_at_categories(df).to_json()
    }

with open('data/processed/metrics.json', 'w') as f:
        f.write(json.dumps(json_output))

#['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']

df_stock_codes = df[['StockCode', 'Description', 'UnitPrice']].drop_duplicates(subset='StockCode').reset_index(drop=True)
df_invoices = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates(subset='InvoiceNo').reset_index(drop=True)
df_invoice_itens = df[['InvoiceNo','Quantity', 'StockCode','UnitPrice']]
df_costumers = df[['CustomerID', 'Country']].drop_duplicates(subset='CustomerID').reset_index(drop=True)
df_costumers = df_costumers.dropna(subset=['CustomerID'])
df_costumers['CustomerID'] = df_costumers['CustomerID'].astype(int)
print('-'*30)
print(df_stock_codes.head(5))
print('-'*30)
print(df_invoices.head(5))
print('-'*30)
print(df_invoice_itens.head(5))
print('-'*30)
print(df_costumers.head(5))

conection = sqlite3.connect('database.db')
cursor = conection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute(
     '''CREATE TABLE IF NOT EXISTS customers(
        CustomerID TEXT PRIMARY KEY,
        Country TEXT
     )
     '''
)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        StockCode TEXT PRIMARY KEY,
        Description TEXT,
        UnityPrice REAL
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices(
    InvoiceNo TEXT PRIMARY KEY,
    InvoiceDate TEXT,
    CustomerID TEXT,
    FOREIGN KEY (CustomerID) REFERENCES customers (CustomerID)
    )

''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        InvoiceNo TEXT,
        StockCode TEXT,
        Quantity INTEGER,
        UnitPrice REAL,
        FOREIGN KEY (InvoiceNo) REFERENCES invoices(InvoiceNo),
        FOREIGN KEY (StockCode) REFERENCES products(StockCode)
    )
''')

df_stock_codes.to_sql('products', conection, if_exists='replace', index=False)
df_invoices.to_sql('invoices', conection, if_exists='replace', index=False)
df_invoice_itens.to_sql('invoice_items', conection, if_exists='replace', index=False)
df_costumers.to_sql('customers', conection, if_exists='replace', index=False)
cursor.close()