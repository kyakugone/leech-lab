import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WANIKANI_TOKEN")

url = "https://api.wanikani.com/v2/review_statistics"
records = []

while url:
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    records.extend(data["data"])
    url = data["pages"]["next_url"]

print(len(records))

leeches = []

for record in records:
    stats = record["data"]
    incorrect = max(stats["meaning_incorrect"], stats["reading_incorrect"])
    streak = min(stats["meaning_current_streak"], stats["reading_current_streak"])
    if streak > 0:
        score = incorrect / (streak ** 1.5)
        if score >= 1.0 and incorrect >= 3:
            leeches.append((score, stats["subject_id"], stats["subject_type"], incorrect, streak))

leeches.sort(reverse=True)

print(len(leeches))
top = leeches[:20]

ids = []
for leech in top:
    ids.append(str(leech[1]))

response = requests.get(
    "https://api.wanikani.com/v2/subjects",
    headers={"Authorization": f"Bearer {token}"},
    params={"ids": ",".join(ids)},
)

subjects = {}
for subject in response.json()["data"]:
    subjects[subject["id"]] = subject["data"]

for leech in top:
    info = subjects[leech[1]]
    print(info["characters"], info["readings"][0]["reading"], info["meanings"][0]["meaning"], leech[0])    