from env.tasks import TASKS
from env.grader import evaluate_response

class CustomerSupportEnv:
    def __init__(self):
        self.current_task = None
        self.step_count = 0

    def reset(self):
        import random
        self.current_task = random.choice(TASKS)
        self.step_count = 0

        return {
            "ticket_id": self.current_task["id"],
            "message": self.current_task["message"],
            "history": [],
            "step_count": self.step_count
        }

    def step(self, action):
        self.step_count += 1

        response = action.get("content", "")

        reward = evaluate_response(
            self.current_task["message"],
            response,
            self.current_task["solution_keywords"]
        )

        done = reward > 0

        state = {
            "ticket_id": self.current_task["id"],
            "message": self.current_task["message"],
            "history": [response],
            "step_count": self.step_count
        }

        return [state, reward, done, {}]
