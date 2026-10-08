import requests
import json
import sys

QWEN_ENDPOINT = "http://192.168.1.89:1234/v1/chat/completions"
MODEL_NAME = "unsloth/qwen3.8-27b"

def query_qwen(prompt, system_prompt="You are an expert full-stack developer and creative director assisting with an Astro + Tailwind website for a Portuguese wine and olive oil estate.", temperature=0.7):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }
    try:
        r = requests.post(QWEN_ENDPOINT, json=payload, timeout=120)
        if r.status_code == 200:
            res = r.json()
            return res['choices'][0]['message']['content']
        else:
            return f"Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"Request failed: {e}"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        print(query_qwen(user_prompt))
    else:
        print("Usage: python qwen_bridge.py 'Your prompt here'")
