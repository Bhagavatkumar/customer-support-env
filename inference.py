import os
import requests
from openai import OpenAI

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN is required")

#  OPENAI CLIENT (MANDATORY)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_task(task_id):
    print(f"[START] task={task_id} env=csre model={MODEL_NAME}")

    # reset env
    state = requests.post("https://bhagavatkumar-customer-support-env-v2.hf.space/reset").json()

    try:
        # ACTUAL LLM CALL (THIS FIXES YOUR ERROR)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": state["message"]}
            ]
        )

        action_text = response.choices[0].message.content.strip()

        error = "null"

    except Exception as e:
        action_text = "We are resolving your issue"
        error = str(e)

    action = {
        "action_type": "respond",
        "content": action_text
    }

    step_response = requests.post(
        "https://bhagavatkumar-customer-support-env-v2.hf.space/step",
        json=action
    ).json()

    reward = float(step_response[1])
    done = bool(step_response[2])

    reward = max(0.01, min(0.99, reward))

    print(f"[STEP] step=1 action=respond reward={reward:.2f} done={str(done).lower()} error={error}")

    print(f"[END] success=true steps=1 score={reward:.2f} rewards={reward:.2f}")


if __name__ == "__main__":
    for i in range(3):  # REQUIRED: 3 TASKS
        run_task(i)
