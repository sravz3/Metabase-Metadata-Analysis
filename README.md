# 📊 Metabase Metadata Analysis with Python

This repository demonstrates how to use the Metabase API to extract and analyze metadata across your Metabase workspace. The goal is to empower data teams to proactively manage and audit dashboards, questions, and collections—especially in growing environments where dashboards can easily go stale or break silently.

By querying key API endpoints like `cards`, `databases`, and `collections`, we generate a master dataset that helps you understand:

- What analyses (cards) exist
- Which databases and collections they belong to
- How to manage and organize content at scale

👉 [Read the full article on Medium](https://medium.com/zenjob-tech-blog/metabase-data-management-made-easy-with-python-a332d4c364e3)

---

## 🚀 Features

- Connects to Metabase using API authentication
- Fetches metadata from:
  - `/api/card` (questions/dashboards)
  - `/api/database` (data source metadata)
  - `/api/collection` (organizational groupings)
- Creates a unified metadata table to trace content lineage
- Customizable scripts to support content cleanup, analysis auditing, and documentation

---

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/metabase-metadata-analysis.git
   cd metabase-metadata-analysis
   ```

2. **Create an API key in Metabase**  
   Follow the instructions in the official docs:  
   👉 [Metabase API Key Setup](https://www.metabase.com/docs/latest/people-and-groups/api-keys)

3. **Update credentials in your script**
   ```python
   API_KEY = '<YOUR_API_KEY>'
   BASE_URL = 'https://your-org.metabase.com'
   ```

---

## ▶️ Usage

Run the script to extract metadata and save results:

```bash
python main.py
```

You will get a consolidated output (e.g., `metabase_metadata.csv` or a DataFrame) that can be explored further using Pandas or exported to a BI tool.

---

## 🛠️ Extend and Customize

This is just a foundation. You can build additional utilities on top of the metadata, including:

- Detecting broken or unused dashboards
- Auditing content owners
- Identifying duplicate or outdated analyses
- Sending automated alerts for at-risk dashboards
- Visualizing content growth and usage over time

