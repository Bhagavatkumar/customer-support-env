from env.tasks import TASKS
from env.grader import grade

import random

class CustomerSupportEnv:
    def __init__(self):
        self.current_task = None
        self.step_count = 0
        self.history = []

    def reset(self):
        self.current_task = random.choice(TASKS)
        self.step_count = 0
        self.history = []

        return {
            "ticket_id": self.current_task["id"],
            "message": self.current_task["message"],
            "history": self.history,
            "step_count": self.step_count
        }

    def state(self):
        return {
            "ticket_id": self.current_task["id"],
            "message": self.current_task["message"],
            "history": self.history,
            "step_count": self.step_count
        }

    def step(self, action):
        self.step_count += 1

        # IMPORTANT: full action store
        self.history.append({
            "action_type": action.get("action_type", ""),
            "content": action.get("content", "")
        })

        #  grader call
        reward = grade(self.current_task, self.history)

        done = reward > 0.5

        return [
            {
                "ticket_id": self.current_task["id"],
                "message": self.current_task["message"],
                "history": self.history,
                "step_count": self.step_count
            },
            reward,
            done,
            {}
        ]
