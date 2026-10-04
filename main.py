import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WANIKANI_TOKEN")

response = requests.get(
    "https://api.wanikani.com/v2/review_statistics",
    headers={"Authorization": f"Bearer {token}"},
)

data = response.json()

for record in data["data"]:
    stats = record["data"]
    incorrect = max(stats["meaning_incorrect"], stats["reading_incorrect"])
    streak = min(stats["meaning_current_streak"], stats["reading_current_streak"])
    if streak > 0:
        score = incorrect / (streak ** 1.5)
        if score >= 1.0:
            print(stats["subject_id"], stats["subject_type"], incorrect, streak, round(score, 2))