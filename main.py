# Import all necessary libraries
import requests
import pandas as pd

# Establish connection to the Metabase API
# Create your Metabase API key under admin settings
API_KEY = "YOUR_KEY_HERE"
BASE_URL = "BASE_URL_HERE"  

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

response = requests.get(f"{BASE_URL}/api/card", headers=headers)

if response.ok:
    print("Connection established successfully!")
else:
    print(f"Error {response.status_code}: {response.text}")


# Fetch all the questions in your site
data = response.json()
print(f"Fetched {len(data)} cards")

# Lets fetch and transform the response only for the fields we need - name, type, query_type, creator, creator_email, view_count, 
# database_id, collection_id, created_at, last_used_at, updated_at, query_text
records = []
for item in data:
    creator = item.get('creator', {})
    dataset_query = item.get('dataset_query', {})
    native_query = dataset_query.get('native', {})

    records.append({
        'view_count': item.get('view_count'),
        'creator': f"{creator.get('first_name', '')} {creator.get('last_name', '')}".strip(),
        'creator_email': creator.get('email'),
        'database_id': item.get('database_id'),
        'collection_id': item.get('collection_id'),
        'name': item.get('name'),
        'last_used_at': item.get('last_used_at'),
        'type': item.get('type'),
        'updated_at': item.get('updated_at'),
        'query_type': dataset_query.get('type'),
        'query_text': native_query.get('query'),
        'created_at': item.get('created_at')
    })

# Convert all the questions to DataFrame
df = pd.DataFrame(records)

# Fetch the databases information
response2 = requests.get(f"{BASE_URL}/api/database", headers=headers)
if response2.ok:
    db_payload = response2.json()
    db_list = db_payload.get("data", [])
    db_df = pd.DataFrame(db_list)
    # Keeping only the required fields id and name
    db_df = db_df[['id','name']]
    db_df.rename(columns={'id':'database_id','name':'database_name'}, inplace=True)
else:
    print(f"Error fetching databases: {response2.status_code} - {response2.text}")

# Fetch all collections information
response3 = requests.get(f"{BASE_URL}/api/collection", headers=headers)

# Step 2: Parse and convert to DataFrame
if response3.ok:
    collections_payload = response3.json()
    df_collections = pd.DataFrame(collections_payload)
else:
    print(f"Error fetching collections: {response3.status_code} - {response3.text}")

# Create a dictionary to lookup the collection name
id_to_name = dict(zip(df_collections["id"], df_collections["name"]))

# We also want to extract the parent collection name. In our case, "parent_id" is always null
# So we look at "location" to fetch the parent collection name
def get_parent_name(collection_id):
    res = requests.get(f"{BASE_URL}/api/collection/{collection_id}", headers=headers)
    if not res.ok:
        return None

    data2 = res.json()
    location = data2.get("location")  # e.g. "/1317/1332/"
    if location:
        # Safely split and filter out empty strings
        parts = [int(x) for x in location.strip("/").split("/") if x.strip().isdigit()]
        if len(parts) >= 2:
            parent_id = parts[-2]
            return id_to_name.get(parent_id)
    return None

df_collections["parent_name"] = df_collections["id"].apply(get_parent_name)

# Renaming columns
df_collections = df_collections[['id','name','parent_name']]
df_collections.rename(columns={'id':'collection_id','name':'collection_name'}, inplace=True)

## Merge everything together to create a Master Dataset
df = pd.merge(df, db_df, how='left', on= 'database_id')
df = pd.merge(df, df_collections, how='left', on= 'collection_id')

# Save to excel file
df.to_excel("Metabase Raw data.xlsx", index=False)