from openai import OpenAI
import os

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def grade(task, actions):
    response = " ".join([a.get("content", "") for a in actions])

    prompt = f"""
You are a strict evaluator.

User problem:
{task['message']}

Expected solution:
{task['solution_keywords']}

Agent response:
{response}

Score strictly between 0 and 1.
Only return a number.
"""

    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        score = float(res.choices[0].message.content.strip())
        return max(0.01, min(score, 0.99))

    except:
        return 0.5
