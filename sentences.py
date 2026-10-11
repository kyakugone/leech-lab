import os
import json
import anthropic
import psycopg
import random
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

RED = "\033[31m"
RESET = "\033[0m"

with open("leeches.sql") as f:
    query = f.read()

with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
    leeches = conn.execute(query).fetchall()


def make_passage(group):
    words = []
    for leech in group:
                words.append(f"{leech[0]} ({leech[1]}): {leech[2]} [{leech[6]}]")
    word_list = "\n".join(words)
    print(word_list)

    prompt = f"""I'm studying for JLPT N2. These are words I keep getting wrong on WaniKani:

{word_list}

Write one cohesive paragraph in the style of a JLPT N2 reading comprehension passage that uses every one of these words naturally. Wrap each of these words, in whatever form it appears, in double square brackets like [[雇った]].

Each item is labelled [vocabulary] or [kanji]. Use vocabulary items as they are. For kanji items, do not use the kanji as a standalone word. Instead, use a common word that contains that kanji read with the listed reading, for example 車輪 for 輪 (りん), and wrap that whole word in the double square brackets.

Then write one comprehension question about the passage in Japanese, in the style of JLPT N2, with four answer choices in Japanese. Do not use the double square brackets in the question or choices.

Respond with only JSON, no other text, in this shape:
{{"sentences": [{{"japanese": "...", "english": "..."}}], "question": "...", "choices": ["...", "...", "...", "..."], "answer": 1}}

"answer" is the number of the correct choice, from 1 to 4."""

    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""
    for block in message.content:
        if block.type == "text":
            text += block.text
    text = text.strip().removeprefix("```json").removesuffix("```")
    passage = json.loads(text)

    print()
    for sentence in passage["sentences"]:
        print(sentence["japanese"].replace("[[", RED).replace("]]", RESET))

    print()
    correct = passage["choices"][passage["answer"] - 1]
    random.shuffle(passage["choices"])
    answer = passage["choices"].index(correct) + 1
    print(passage["question"])
   
    number = 1
    for choice in passage["choices"]:
        print(f"{number}. {choice}")
        number += 1

    guess = input("Your answer (1-4): ")
    if int(guess) == answer:
        print("正解!")
    else:
        print(f"The answer was {answer}.")

    print()
    for sentence in passage["sentences"]:
        print(sentence["english"])


for start in range(0, 20, 5):
    make_passage(leeches[start:start + 5])
    print("-" * 40)