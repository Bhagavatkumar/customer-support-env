import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://bhagavatkumar-customer-support-env-v2.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key=HF_TOKEN
)

def run_episode():
    task = "customer-support"
    env_name = "csre"

    print(f"[START] task={task} env={env_name} model={MODEL_NAME}")

    state = requests.post(f"{API_BASE_URL}/reset").json()

    done = False
    step = 0
    rewards = []

    while not done:
        step += 1

        # simple LLM call (compliance)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": state["message"]}]
        )

        action_text = response.choices[0].message.content[:50]

        action = {
            "action_type": "respond",
            "content": action_text
        }

        state, reward, done, info = requests.post(
            f"{API_BASE_URL}/step", json=action
        ).json()

        rewards.append(reward)

        print(
            f"[STEP] step={step} action={action_text} "
            f"reward={reward:.2f} done={str(done).lower()} error=null"
        )

    success = rewards[-1] > 0

    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step} rewards={rewards_str}"
    )


if __name__ == "__main__":
    run_episode()
