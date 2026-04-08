import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "https://bhagavatkumar-customer-support-env-v2.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline")
HF_TOKEN = os.getenv("HF_TOKEN")

def run_episode():
    print(f"[START] task=csre env=customer-support model={MODEL_NAME}")

    state = requests.post(f"{API_BASE_URL}/reset").json()

    done = False
    step = 0
    rewards = []

    while not done:
        step += 1

        # FIX: safe handling (NO state["message"])
        if isinstance(state, dict):
            message = state.get("message", "")
        else:
            message = ""

        action = {
            "action_type": "respond",
            "content": "I will help you resolve your issue"
        }

        response = requests.post(f"{API_BASE_URL}/step", json=action).json()

        # FIX: correct unpack
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
            f"[STEP] step={step} action=respond "
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
