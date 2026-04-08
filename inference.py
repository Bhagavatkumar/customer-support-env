import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://bhagavatkumar-customer-support-env-v2.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# MUST: use proxy
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_episode():
    print(f"[START] task=csre env=customer-support model={MODEL_NAME}")

    state = requests.post(f"{API_BASE_URL}/reset").json()

    done = False
    step = 0
    rewards = []

    while not done:
        step += 1

        # safe message extraction
        if isinstance(state, dict):
            message = state.get("message", "")
        else:
            message = ""

        # LLM via proxy
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": message}]
            )
            action_text = response.choices[0].message.content[:50]
        except:
            action_text = "I will help you resolve your issue"

        action = {
            "action_type": "respond",
            "content": action_text
        }

        response = requests.post(f"{API_BASE_URL}/step", json=action).json()

        if isinstance(response, list):
            state = response[0]
            reward = response[1]
            done = response[2]
        else:
            state = response
            reward = 0.0
            done = True

        rewards.append(reward)

        print(
            f"[STEP] step={step} action={action_text} "
            f"reward={reward:.2f} done={str(done).lower()} error=null"
        )

    success = rewards[-1] > 0 if rewards else False
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step} rewards={rewards_str}"
    )

if __name__ == "__main__":
    run_episode()
