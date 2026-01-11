import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s- %(message)s",
    filemode="a"

)



engine = create_engine('sqlite:///inventory.db')



def load_raw_data():
    '''This function will load the CSVs as dataframe and ingest into db'''
    start=time.time()
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            file_path = os.path.join('data', file)
            table_name = file[:-4]   # remove .csv
            
            print(f"Ingesting {file}...")
            logging.info(f'Ingesting {file} into database')
    
            first = True
            for chunk in pd.read_csv(file_path, chunksize=100_000):
                chunk.to_sql(
                    table_name,
                    engine,
                    if_exists='replace' if first else 'append',
                    index=False
                )
                first = False
    
            print(f"{file} done ✅")
            
    end= time.time()
    total_time =(end-start) / 60
    logging.info('------------------------Ingestion Complete-----------------------')
    logging.info(f'Total Time Taken : {total_time} minutes ')



if __name__ == '__main__' :
    load_raw_data()