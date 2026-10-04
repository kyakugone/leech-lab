import os
import requests
import psycopg
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WANIKANI_TOKEN")
database_url = os.getenv("DATABASE_URL")

url = "https://api.wanikani.com/v2/review_statistics"
records = []

while url:
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    records.extend(data["data"])
    url = data["pages"]["next_url"]

print(len(records))

with psycopg.connect(database_url) as conn:
    conn.execute("TRUNCATE review_statistics")
    for record in records:
        stats = record["data"]
        conn.execute(
            "INSERT INTO review_statistics VALUES (%s, %s, %s, %s, %s, %s)",
            (
                stats["subject_id"],
                stats["subject_type"],
                stats["meaning_incorrect"],
                stats["reading_incorrect"],
                stats["meaning_current_streak"],
                stats["reading_current_streak"]

            ),
        )

print("Loaded")