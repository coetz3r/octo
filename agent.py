import json
import os
import random
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Menory class
class Memory:
    def __init__(self):
        self.filename = os.path.join(BASE_DIR, "memory.json")
        self.experiences = []
        self.load()

    def store(self, experience):
        self.experiences.append(experience)
        self.save()

    def novelty(self, stimulus):
        count = sum(1 for e in self.experiences if e["stimulus"] == stimulus)
        return 1.0 / (1 + count)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.experiences, f, indent=2)

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.experiences = json.load(f)
            except json.JSONDecodeError:
                self.experiences = []

# value class
class Values:
    def __init__(self):
        self.filename = os.path.join(BASE_DIR, "values.json")
        self.values = {}
        self.load()

    def get(self, key):
        return self.values.get(key, 0.0)

    def update(self, key, reward, lr=0.1):
        self.values[key] = self.get(key) + lr * reward
        self.save()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.values, f, indent=2)

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.values = json.load(f)
            except json.JSONDecodeError:
                self.values = {}

# Agent class
class Agent:
    def __init__(self):
        self.memory = Memory()
        self.values = Values()

        self.head_x = 0.0
        self.head_y = 0.0

        # PUBLIC STATE (GUI READS ONLY)
        self.state = {
            "stimulus": None,
            "action": None,
            "reward": 0.0,
            "head": {"x": 0.0, "y": 0.0}
        }

    def perceive(self):
        return {
            "type": "visual",
            "x": random.uniform(-1, 1),
            "y": random.uniform(-1, 1)
        }

    def appraise(self, stimulus):
        novelty = self.memory.novelty(stimulus)
        return novelty

    def decide(self, stimulus):
        actions = ["look_left", "look_right", "look_up", "look_down", "idle"]
        return max(actions, key=lambda a: self.values.get(a) + random.random() * 0.1)

    def act(self, action, stimulus):
        if action == "look_left":
            self.head_x -= 0.1
        elif action == "look_right":
            self.head_x += 0.1
        elif action == "look_up":
            self.head_y += 0.1
        elif action == "look_down":
            self.head_y -= 0.1

        self.head_x = max(-1, min(1, self.head_x))
        self.head_y = max(-1, min(1, self.head_y))

    def reward(self, stimulus):
        distance = abs(stimulus["x"] - self.head_x) + abs(stimulus["y"] - self.head_y)
        return 1.0 - distance

    def step(self):
        stimulus = self.perceive()
        appraisal = self.appraise(stimulus)
        action = self.decide(stimulus)
        self.act(action, stimulus)
        reward = self.reward(stimulus)

        self.memory.store({"stimulus": stimulus, "action": action, "reward": reward})
        self.values.update(action, reward)

        # Update public state
        self.state["stimulus"] = stimulus
        self.state["action"] = action
        self.state["reward"] = reward
        self.state["head"] = {"x": self.head_x, "y": self.head_y}


if __name__ == "__main__":
    agent = Agent()
    while True:
        agent.step()
        time.sleep(0.2)
