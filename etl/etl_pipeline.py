
import pandas as pd, os
def run_etl():
    raw = 'data/raw/transactions_raw.csv'
    out = 'data/processed/transactions.csv'
    if os.path.exists(raw):
        df = pd.read_csv(raw)
        df.to_csv(out, index=False)
        print('ETL done, wrote', out)
    else:
        print('Raw transactions not found at', raw)
if __name__=='__main__':
    run_etl()
