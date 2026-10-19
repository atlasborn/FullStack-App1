from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
import pandas as pd
import json
import sqlite3
'''

○ Endpoints:
■ GET /tickets (lista simples)
■ PATCH /tickets/{id} (alterar status ou priority)
■ GET /metrics (retorna métricas prontas em arquivo gerado pelo
pandas)
○ Seeds: ~20 tickets inseridos ao iniciar (pode ser de um .json).
○ Persistência em SQLite (um arquivo .db).

'''

def get_data()-> pd.DataFrame:
    conection = sqlite3.connect('database.db')
    cursor = conection.cursor()
    query = """
        SELECT 
            i.InvoiceNo,
            ii.StockCode,
            p.Description,
            ii.Quantity,
            i.InvoiceDate,
            ii.UnitPrice,
            i.CustomerID,
            c.Country
        FROM invoice_items ii
        JOIN invoices i ON ii.InvoiceNo = i.InvoiceNo
        JOIN products p ON ii.StockCode = p.StockCode
        LEFT JOIN customers c ON i.CustomerID = c.CustomerID
    """

    df = pd.read_sql(query, conection)
    conection.close()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

    return df

# df.to_sql('ecommerce', conection, if_exists='replace', index=False)
# cursor.close()

class Metrics:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.profit_days = self.profit_per_day()
        self.profit_categories = self.profit_at_categories()
    
    def profit_per_day(self) -> pd.DataFrame:
        df_copy = self.df.copy()
        df_copy['Profit'] = df_copy['Quantity'] * df_copy['UnitPrice']
        sells = df_copy.groupby(df_copy['InvoiceDate'].dt.date)['Profit'].sum().reset_index(name='Profit')
        return sells.to_dict(orient='records')
    def profit_at_categories(self) -> pd.DataFrame:
        df_copy = self.df.copy()
        df_copy['UnitPrice'] = pd.to_numeric(df_copy['UnitPrice'])
        df_copy['Quantity'] = pd.to_numeric(df_copy['Quantity'])
        df_copy['Profit'] = df_copy['UnitPrice']  * df_copy['Quantity']
        sells = df_copy.groupby(df_copy['Description'])['Profit'].sum().reset_index(name='Profit')
        sells.sort_values(by='Profit', ascending=False, inplace=True)
        return sells.to_dict(orient='records')

origins = [
    "http://localhost:3000",  # Libera o seu Next.js
    "http://127.0.0.1:3000"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def home():
    return {'status': 'you are in home'}

@app.get("/tickets")
async def tickets():
    pass

@app.get("/metrics")
async def cal_metrics():
    df = get_data()
    metrics = Metrics(df)
    metrics_json = {
        'profit_days': metrics.profit_days,
        'profit_categories': metrics.profit_categories
    }
    print(metrics_json)
    return metrics_json

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)