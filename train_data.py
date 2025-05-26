
import urllib.request
import urllib.parse
import pandas as pd
import json
import time
url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=6cf35ec2-c0eb-4ef0-a904-f093dab0abfd&q=שדרות'  
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
train_df.to_csv("train_data.csv", index=False, encoding="utf-8-sig")