import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WANIKANI_TOKEN")

response = requests.get(
    "https://api.wanikani.com/v2/user",
    headers={"Authorization": f"Bearer {token}"},
)

data = response.json()
print(data["data"]["username"])
print(data["data"]["level"])


