import pandas as pd
from sqlalchemy import create_engine
import ast

ENVELOPE_PATH = r"data/muatzut.txt"

def get_btl_data():

    # URL of the webpage containing the table
    url = "https://www.btl.gov.il/mediniyut/situation/statistics/btlstatistics.aspx?type=2&id=8"
    ENVELOPE_PATH = r"data/muatzut.txt"
    # Read all tables from the webpage
    tables = pd.read_html(url)

    # If at least one table is found, proceed to save the first one
    if tables:
        print(f"Number of tables found: {len(tables)}")
        # Select the first table
        df = tables[1]
        # Save the DataFrame to a CSV file
        engine = create_engine('postgresql+psycopg2://postgres:Aa123456@10.0.70.12:5432/homecoming')
        df.to_sql("unemployment" + '_data', engine, if_exists='replace', index=False)
        file = open(ENVELOPE_PATH, "r", encoding = "utf-8")
        envelope_string = file.read()
        hebrew_list = ast.literal_eval(envelope_string)
        df = df[df["ישוב"].isin(hebrew_list)]
        df.to_csv(r"data\unemployment_statistics.csv", index=False, encoding="utf-8-sig")
        engine = create_engine('postgresql+psycopg2://postgres:Aa123456@10.0.70.12:5432/homecoming')
        df.to_sql("unemployment_statistics", engine, if_exists='replace', index=False)
        print("BTL data saved to database.")
    else:
        print("No tables found on the webpage.")