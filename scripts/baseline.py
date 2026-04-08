from env.core import CustomerSupportEnv

env = CustomerSupportEnv()

def run_agent():
    obs = env.reset()
    total_reward = 0

    for _ in range(5):
        action = {
            "action_type": "respond",
            "content": "I will help you resolve this issue"
        }

        obs, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward

if __name__ == "__main__":
    score = run_agent()
    print("Baseline Score:", score)
