# filename: chat_with_ollama.py

import requests
import json

def chat_with_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Authorization": "Bearer ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOP3LFYgbGp0qJZouYWVBpZ6ey7YMw7UsPs09U7NSeU"
    }
    data = {
        "model": "tinyllama",
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_parts = response.text.split("\n")
    for part in response_parts:
        if part:
            print(json.loads(part)["response"], end="")

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            break
        print("Ollama: ", end="")
        chat_with_ollama(user_input)