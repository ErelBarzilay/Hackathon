
import urllib.request
import urllib.parse
import pandas as pd
import json
import ssl
import ast
from sqlalchemy import create_engine

ENVELOPE_PATH = r"data/gaza_envelope.txt"
BUS_PATH = r"data/bus_envelope.txt"
TRAIN_PATH = r"."
def pop_func(db, gaza_envelope, *args):
    file = open(gaza_envelope, "r", encoding = "utf-8")
    envelope_string = file.read()
    hebrew_list = ast.literal_eval(envelope_string)
    for i in range(len(hebrew_list)):
        hebrew_list[i] += " "
    db = db[db["שם_ישוב"].isin(hebrew_list)]
    return db
    
def bus_func(db, envelope, *args):
    file = open(envelope, "r", encoding = "utf-8")
    envelope_string = file.read()
    hebrew_list = ast.literal_eval(envelope_string)
    db = db[db["cluster_nm"].isin(hebrew_list)]
    grouped_df = db.groupby(['ClusterId', 'cluster_nm', 'trip_year', 'trip_month'], as_index=False)[['hakdama', 'eibizua', 'eihurim', 'takin']].sum()
    return grouped_df

def train_func(db, _,*args):
    grouped_df = db.groupby(['first_train_station_nm', 'last_train_station_nm', 'shana', 'hodesh'], as_index = False)[['rishui_all', 'rishui_only', 'bitzua_only']].sum()
    return grouped_df

def main():
    context = ssl._create_unverified_context()
    RESOURCE_IDS = {
        "population": ("64edd0ee-3d5d-43ce-8562-c336c24dbc1f", pop_func, ENVELOPE_PATH), 
        "bus": ("86eceab6-44ac-4301-a6a7-9a4a92dae48b", bus_func, BUS_PATH), 
        "train": ("6cf35ec2-c0eb-4ef0-a904-f093dab0abfd&q=שדרות", train_func, TRAIN_PATH)
        }
    for key in RESOURCE_IDS:
        url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=' + RESOURCE_IDS[key][0]
        parsed_url = urllib.parse.urlsplit(url)
        encoded_query = urllib.parse.quote(parsed_url.query, safe="=&")  # keep '=' and '&' for query
        encoded_url = urllib.parse.urlunsplit((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            encoded_query,
            parsed_url.fragment
        ))
        # Now open the encoded URL
        fileobj = urllib.request.urlopen(encoded_url, context=context)
        json_val = json.loads(fileobj.read().decode('utf-8'))["result"]["records"]
        df = pd.DataFrame(json_val)
        df = RESOURCE_IDS[key][1](df, RESOURCE_IDS[key][2])
        df.to_csv("data/" + key + "_data.csv", index=False, encoding="utf-8-sig")
        engine = create_engine('postgresql+psycopg2://postgres:Aa123456@10.0.70.12:5432/homecoming')
        df.to_sql(key + '_data', engine, if_exists='replace', index=False)
        
if __name__ == "__main__":
    main()
