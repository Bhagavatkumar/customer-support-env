import requests

BASE_URL = "https://bhagavatkumar-customer-support-env-v2.hf.space"

def run_episode():
    state = requests.get(f"{BASE_URL}/reset").json()
    
    done = False
    total_reward = 0

    print("[START]", state)

    while not done:
        action = {
            "action_type": "respond",
            "content": "I will help you reset your password quickly"
        }

        response = requests.post(f"{BASE_URL}/step", json=action).json()

        state, reward, done, info = response

        total_reward += reward

        print("[STEP]", state, reward, done)

    print("[END] Total Reward:", total_reward)

if __name__ == "__main__":
    run_episode()