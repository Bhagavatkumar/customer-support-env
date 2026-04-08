from env.tasks import TASKS
from env.grader import grade
import random

class CustomerSupportEnv:
    def __init__(self):
        self.current_task = None
        self.step_count = 0

    def reset(self):
        self.current_task = random.choice(TASKS)
        self.step_count = 0

        return {
            "ticket_id": self.current_task["id"],
            "message": self.current_task["message"],
            "history": [],
            "step_count": self.step_count
        }

    def state(self):
        return {
            "ticket_id": self.current_task["id"],
            "message": self.current_task["message"],
            "history": [],
            "step_count": self.step_count
        }

    def step(self, action):
        self.step_count += 1

        #  ALWAYS evaluate current action
        reward = grade(self.current_task, [action])

        #  ALWAYS finish task in one step (CRITICAL FOR VALIDATOR)
        done = True

        return [
            {
                "ticket_id": self.current_task["id"],
                "message": self.current_task["message"],
                "history": [action],
                "step_count": self.step_count
            },
            reward,
            done,
            {}
        ]
