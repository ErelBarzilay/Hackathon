
import urllib.request
import urllib.parse
import pandas as pd
import json
import os
os.chdir("data")
RESOURCE_IDS = {"population": "64edd0ee-3d5d-43ce-8562-c336c24dbc1f", "bus": "86eceab6-44ac-4301-a6a7-9a4a92dae48b", "train": "6cf35ec2-c0eb-4ef0-a904-f093dab0abfd"}
for key in RESOURCE_IDS:
    url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=' + RESOURCE_IDS[key]  
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
    fileobj = urllib.request.urlopen(encoded_url)
    json_val = json.loads(fileobj.read().decode('utf-8'))["result"]["records"]
    train_df = pd.DataFrame(json_val)
    train_df.to_csv(key + "_data.csv", index=False, encoding="utf-8-sig")
