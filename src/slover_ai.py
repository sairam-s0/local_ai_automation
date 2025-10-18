# src/slover_ai.py
import requests
import json

def generate_with_phi(prompt):
    url = "http://127.0.0.1:11434/api/generate"
    data = {"model": "phi3", "prompt": prompt}
    response = requests.post(url, json=data)
    
    # Split response by lines (each line is a JSON object)
    full_text = ""
    for line in response.text.strip().split("\n"):
        try:
            obj = json.loads(line)
            if "response" in obj:
                full_text += obj["response"]
        except json.JSONDecodeError:
            continue
    
    return full_text.strip()

# Test
question = "Question: What is 2 + 2?\nOptions:\nA. 3\nB. 4\nC. 5\nSelect the correct option."
answer = generate_with_phi(question)
print("Phi answer:", answer)
