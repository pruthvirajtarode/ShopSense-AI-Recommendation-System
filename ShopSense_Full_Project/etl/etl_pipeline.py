
import pandas as pd

def run_etl():
    df = pd.read_csv('data/raw/online_retail.csv')
    df = df.dropna(subset=['InvoiceNo','StockCode'])
    df.to_csv('data/processed/transactions.csv', index=False)

if __name__ == '__main__':
    run_etl()
