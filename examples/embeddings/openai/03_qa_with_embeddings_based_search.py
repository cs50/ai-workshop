from openai import OpenAI
import json
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_embedding(text, model="text-embedding-3-small"):

    text = text.replace("\n", " ")

    return client.embeddings.create(input=[text], model=model).data[0].embedding


with open('embeddings.jsonl', 'r') as f:

    lines = f.readlines()

    embeddings = {}

    for line in lines:

        line = json.loads(line)

        embeddings[line['text']] = line['embedding']


system_prompt = "You are a friendly and supportive teaching assistant for CS50. You are also a cat."


user_query = input("User: ")


query_embedding = get_embedding(user_query)


best_chunk = None
best_score = float("-inf")


for chunk, embedding in embeddings.items():

    score = np.dot(embedding, query_embedding)

    if score > best_score:
        best_chunk = chunk
        best_score = score


prompt = "Answer the question using the following information delimited by triple brackets:\n\n"
prompt += f"```\n{best_chunk}\n```"
prompt += "\nQuestion: " + user_query

print(f"Prompt:\n\n{prompt}\n")


chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"{prompt}"}
    ],
    model="gpt-4",
)


response_text = chat_completion.choices[0].message.content


print(f"Assistant: {response_text}")
