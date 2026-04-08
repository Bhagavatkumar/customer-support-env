import random
from env.tasks import TASKS

class CustomerSupportEnv:

    def __init__(self):
        self.tasks = TASKS
        self.current_task = None
        self.history = []
        self.step_count = 0
        self.done = False

    def reset(self):
        self.current_task = random.choice(self.tasks)
        self.history = []
        self.step_count = 0
        self.done = False

        return self._get_observation()

    def step(self, action):
        self.step_count += 1
        self.history.append(action)

        reward = self._compute_reward(action)

        # ✅ NEW: close action se episode end
        if action["action_type"] == "close":
            self.done = True

        # max steps condition
        if self.step_count >= 5:
            self.done = True

        return self._get_observation(), reward, self.done, {}

    def state(self):
        return {
            "task": self.current_task,
            "steps": self.step_count
        }

    def _get_observation(self):
        return {
            "ticket_id": self.current_task["id"],
            "message": self.current_task["message"],
            "history": self.history,
            "step_count": self.step_count
        }

    def _compute_reward(self, action):
        reward = 0.0
        content = (action.get("content") or "").lower()

        # helpful response
        if "help" in content or "assist" in content:
            reward += 0.2

        # keyword match
        if any(kw in content for kw in self.current_task["solution_keywords"]):
            reward += 0.3

        # penalty for too many steps
        if self.step_count > 4:
            reward -= 0.2

        return reward
