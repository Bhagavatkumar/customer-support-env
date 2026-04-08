import os
import requests

# Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://bhagavatkumar-customer-support-env-v2.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy")
HF_TOKEN = os.getenv("HF_TOKEN")

def run_episode():
    print("[START] Starting new episode")

    # Reset environment (POST required)
    response = requests.post(f"{API_BASE_URL}/reset")
    state = response.json()

    done = False
    total_reward = 0

    print("[STATE]", state)

    while not done:
        # Simple baseline action
        action = {
            "action_type": "respond",
            "content": "I will help you resolve your issue quickly"
        }

        response = requests.post(f"{API_BASE_URL}/step", json=action)
        state, reward, done, info = response.json()

        total_reward += reward

        print("[STEP]")
        print("State:", state)
        print("Reward:", reward)
        print("Done:", done)

    print("[END] Total Reward:", total_reward)


if __name__ == "__main__":
    run_episode()
