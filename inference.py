import os
import requests
from openai import OpenAI

# Required env variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://bhagavatkumar-customer-support-env-v2.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# MUST: OpenAI client via proxy
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_episode():
    task = "customer-support"
    env_name = "csre"

    print(f"[START] task={task} env={env_name} model={MODEL_NAME}")

    # Reset environment
    state = requests.post(f"{API_BASE_URL}/reset").json()

    done = False
    step = 0
    rewards = []

    while not done:
        step += 1

        # Safe message extraction
        if isinstance(state, dict):
            message = state.get("message", "")
        else:
            message = ""

        # LLM call via proxy (MANDATORY)
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": message}]
            )
            action_text = response.choices[0].message.content.strip()
            action_text = action_text[:100] if action_text else "Resolving your issue"
        except Exception as e:
            action_text = "Resolving your issue"
            error_msg = str(e)
        else:
            error_msg = "null"

        action = {
            "action_type": "respond",
            "content": action_text
        }

        # Step execution
        try:
            response = requests.post(f"{API_BASE_URL}/step", json=action).json()
        except Exception as e:
            print(f"[STEP] step={step} action=error reward=0.00 done=true error={str(e)}")
            break

        # Safe unpacking
        if isinstance(response, list) and len(response) >= 3:
            state = response[0]
            reward = float(response[1])
            done = bool(response[2])
        else:
            state = response
            reward = 0.0
            done = True

        rewards.append(reward)

        print(
            f"[STEP] step={step} action={action_text.replace(' ', '_')} "
            f"reward={reward:.2f} done={str(done).lower()} error={error_msg}"
        )

    # Compute success + score
    success = rewards[-1] > 0 if rewards else False
    score = sum(rewards) / len(rewards) if rewards else 0.0
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step} score={score:.2f} rewards={rewards_str}"
    )

if __name__ == "__main__":
    run_episode()
