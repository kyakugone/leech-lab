import os
import json
import anthropic
import psycopg
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

with open("leeches.sql") as f:
    query = f.read()

with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
    leeches = conn.execute(query).fetchall()

words = []
for leech in leeches[:5]:
    words.append(f"{leech[0]} ({leech[1]}): {leech[2]}")

word_list = "\n".join(words)
print(word_list)

prompt = f"""I'm studying for JLPT N2. These are words I keep getting wrong on WaniKani:

{word_list}

Write one cohesive paragraph in the style of a JLPT N2 reading comprehension passage that uses every one of these words naturally. Wrap each of these words, in whatever form it appears, in double square brackets like [[雇った]].

Respond with only JSON, no other text, in this shape:
{{"sentences": [{{"japanese": "...", "english": "..."}}]}}"""

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}],
)

text = ""
for block in message.content:
    if block.type == "text":
        text += block.text
text = text.strip()
text = text.removeprefix("```json").removesuffix("```")
passage = json.loads(text)

RED = "\033[31m"
RESET = "\033[0m"

for sentence in passage["sentences"]:
    print(sentence["japanese"].replace("[[", RED).replace("]]", RESET))

print()
for sentence in passage["sentences"]:
    print(sentence["english"])