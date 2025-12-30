import os
import json
import time
import random

# -------------------
# Memory class
# -------------------
class Memory:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(BASE_DIR, "memory.json")
        self.experiences = []
        self.load()  # Load existing memory

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.experiences = data
                else:
                    self.experiences = []
            except:
                self.experiences = []
        else:
            self.experiences = []

    def store(self, stimulus):
        self.experiences.append(stimulus)
        self.save()

    def novelty(self, stimulus):
        return 1.0 / (1 + sum(1 for e in self.experiences if e == stimulus))

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.experiences, f, indent=2)

# -------------------
# Values class
# -------------------
class Values:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(BASE_DIR, "values.json")
        self.data = {}
        self.load()  # Load existing values

    def update(self, reward):
        for key, val in reward.items():
            self.data[key] = self.data.get(key, 0) + val
        self.save()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.data = data
                else:
                    self.data = {}
            except:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)

# -------------------
# Agent class
# -------------------
class Agent:
    def __init__(self):
        self.memory = Memory()
        self.values = Values()

    def perceive(self):
        # Example stimulus
        return random.choice(["light", "sound", "touch", "movement"])

    def decide(self, stimulus):
        # Example action
        return random.choice(["look", "move", "grab", "wait"])

    def act(self, action):
        print(f"Performing action: {action}")

    def reward(self, stimulus):
        # Example reward system
        return {stimulus: random.random()}

    def step(self):
        stimulus = self.perceive()
        action = self.decide(stimulus)
        self.act(action)

        reward = self.reward(stimulus)
        self.values.update(reward)

        novelty = self.memory.novelty(stimulus)
        self.memory.store(stimulus)

        print(f"Stimulus: {stimulus}, Action: {action}, Novelty: {novelty:.2f}")

# -------------------
# Run headless agent
# -------------------
if __name__ == "__main__":
    agent = Agent()
    while True:
        agent.step()
        time.sleep(0.1)
