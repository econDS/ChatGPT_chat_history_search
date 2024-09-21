import json
import pandas as pd

def process_content(v):
    try:
        message = v.get("message", {})
        author = message.get("author", {})
        role = author.get("role")
        content = message.get("content", {})
        parts = content.get("parts")

        if role == "user":
            content_type = content['content_type']
            index = -1 if content_type == 'multimodal_text' else 0
            content_text = "User: " + parts[index] + "\n"
        elif role == "assistant" and content.get("parts") is not None:
            content_text = "ChatGPT:\n" + parts[0] + "\n"
        else:
            content_text = "ChatGPT:\n" + content["text"] + "\n"
    except KeyError:
        content_text = ""
    return content_text

with open("conversations.json", 'r') as f:
    data = json.load(f)
    
ids, titles, create_times, contents = [], [], [], []

for d in data:
    ids.append(f"https://chat.openai.com/c/{d['id']}")
    titles.append(d["title"] if d["title"] is not None else "")
    create_times.append(d["create_time"])
    content_text = ""
    for v in d['mapping'].values():
        if v["message"] is not None:
            content_text += process_content(v)
    contents.append(content_text)

df = pd.DataFrame({
    "link": ids,
    "titles": titles,
    "create_times": create_times,
    "contents": contents
})
df.to_csv("chat.csv", index=False)
