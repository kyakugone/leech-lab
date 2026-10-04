import os
import requests
import psycopg
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WANIKANI_TOKEN")
database_url = os.getenv("DATABASE_URL")


def fetch_all(url):
    results = []
    while url:
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        data = response.json()
        if "data" not in data:
            print(response.status_code, data)
        results.extend(data["data"])
        url = data["pages"]["next_url"]
    return results


records = fetch_all("https://api.wanikani.com/v2/review_statistics")
print(len(records))

subjects = fetch_all("https://api.wanikani.com/v2/subjects")
print(len(subjects))

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
                stats["reading_current_streak"],
            ),
        )

    conn.execute("TRUNCATE subjects")
    for subject in subjects:
        info = subject["data"]
        reading = None
        if "readings" in info:
            reading = info["readings"][0]["reading"]
        conn.execute(
            "INSERT INTO subjects VALUES (%s, %s, %s, %s, %s)",
            (
                subject["id"],
                subject["object"],
                info["characters"],
                info["meanings"][0]["meaning"],
                reading,
            ),
        )

print("Loaded")