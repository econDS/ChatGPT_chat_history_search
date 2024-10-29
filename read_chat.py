import json
import pandas as pd

def process_content(message_data):
    try:
        message = message_data.get("message", {})
        author = message.get("author", {})
        role = author.get("role")
        content = message.get("content", {})
        parts = content.get("parts", [])

        # Define prefix based on the role
        prefix = ""
        if role == "user":
            prefix = "User: "
            content_type = content.get('content_type', '')
            index = -1 if content_type == 'multimodal_text' else 0
            part = parts[index] if len(parts) > index else {}
            
            if isinstance(part, dict):
                if part.get('content_type') == 'audio_transcription':
                    text = part.get('text', '')
                else:
                    text = part.get('text', part)
            else:
                text = part
            content_text = f"{prefix}{text}\n"

        elif role == "assistant":
            prefix = "ChatGPT: "
            if not parts:
                # Handle case where parts are missing for assistant
                text = content.get("text", "")
                content_text = f"{prefix}{text}\n"
            else:
                part = parts[0]
                if isinstance(part, dict):
                    content_type = part.get('content_type')
                    if content_type == 'audio_transcription':
                        text = part.get('text', '')
                    elif content_type == 'audio_asset_pointer':
                        text = 'Cannot translate audio.'
                    else:
                        text = part.get('text', '')
                else:
                    text = part
                content_text = f"{prefix}{text}\n"
        else:
            # Handle other roles or missing roles
            content_text = ""

        return content_text

    except Exception as e:
        print(f"Error processing content: {e}")
        return ""


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
