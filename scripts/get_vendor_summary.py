import pandas as pd
import sqlite3
import logging
import numpy as np

# -------------------------------------------------------------------
# Logging configuration 
# -------------------------------------------------------------------
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# -------------------------------------------------------------------
# Create Vendor Summary
# -------------------------------------------------------------------
def create_vendor_summary(conn):
    """
    This function creates the vendor summary by aggregating
    sales, purchases, prices, and freight data.
    """

    query ="""
        WITH sales_agg AS (
            SELECT
                VendorNo,
                Brand,
                SUM(SalesDollars) AS TotalSalesDollars,
                SUM(SalesPrice) AS TotalSalesPrice,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        ),
        price_agg AS (
            SELECT
                Brand,
                MAX(Volume) AS Volume,
                MAX(Price) AS ActualPrice
            FROM purchase_prices
            GROUP BY Brand
        ),
        purchase_agg AS (
            SELECT
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            WHERE p.PurchasePrice > 0
            GROUP BY
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.PurchasePrice
        ),
        freight_agg AS (
            SELECT
                VendorNumber,
                SUM(Freight) AS TotalFreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        )
        SELECT
            pa.VendorNumber,
            pa.VendorName,
            pa.Brand,
            pa.Description,
            pa.PurchasePrice,
            pr.Volume,
            pr.ActualPrice,
            pa.TotalPurchaseQuantity,
            pa.TotalPurchaseDollars,
            sa.TotalSalesQuantity,
            sa.TotalSalesDollars,
            sa.TotalSalesPrice,
            sa.TotalExciseTax,
            fa.TotalFreightCost
        FROM purchase_agg pa
        LEFT JOIN price_agg pr
            ON pa.Brand = pr.Brand
        LEFT JOIN sales_agg sa
            ON pa.VendorNumber = sa.VendorNo
           AND pa.Brand = sa.Brand
        LEFT JOIN freight_agg fa
            ON pa.VendorNumber = fa.VendorNumber
    """


    return pd.read_sql_query(query, conn)

# -------------------------------------------------------------------
# Clean & Enrich Data
# -------------------------------------------------------------------
def clean_data(df):
    """
    Cleans the vendor summary data and creates analytical columns.
    """

   
    df["Volume"] = df["Volume"].astype(float)

    # fill missing values
    df.fillna(0, inplace=True)

    # clean text columns
    df["VendorName"] = df["VendorName"].str.strip()
    df["Description"] = df["Description"].astype(str).str.strip()


    # derived metrics 
    df["GrossProfit"] = df["TotalSalesDollars"] - df["TotalPurchaseDollars"]

    df["ProfitMargin"] = np.where(
        df["TotalSalesDollars"] != 0,
        (df["GrossProfit"] / df["TotalSalesDollars"]) * 100,
        0
    )

    df["StockTurnover"] = np.where(
        df["TotalPurchaseQuantity"] != 0,
        df["TotalSalesQuantity"] / df["TotalPurchaseQuantity"],
        0
    )

    df["SalestoPurchaseRatio"] = np.where(
        df["TotalPurchaseDollars"] != 0,
        df["TotalSalesDollars"] / df["TotalPurchaseDollars"],
        0
    )

    
    df.replace([np.inf, -np.inf], 0, inplace=True)

    return df

# -------------------------------------------------------------------
# Ingest Data into SQLite 
# -------------------------------------------------------------------
def ingest_db(df, table_name, conn):
    """
    Inserts cleaned dataframe into SQLite table using cursor.executemany
    """

    cursor = conn.cursor()

    
    df = df.replace([np.inf, -np.inf], None)

    columns = ",".join(df.columns)
    placeholders = ",".join(["?"] * len(df.columns))

    insert_query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
    """

    try:
        cursor.executemany(
            insert_query,
            df.itertuples(index=False, name=None)
        )
        conn.commit()
        logging.info(f"Inserted {len(df)} records into {table_name}")

    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity Error while inserting data: {e}")
        raise

    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        raise

# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------
if __name__ == "__main__":

    conn = sqlite3.connect("inventory.db")

    logging.info("Creating Vendor Summary DataFrame")
    summary_df = create_vendor_summary(conn)
    logging.info(f"Summary rows: {len(summary_df)}")

    logging.info("Cleaning Vendor Summary Data")
    clean_df = clean_data(summary_df)

    logging.info("Ingesting Vendor Summary into Database")
    ingest_db(clean_df, "vendor_sales_summary", conn)

    logging.info("Vendor Summary Pipeline Completed Successfully")
