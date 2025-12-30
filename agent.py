import time
import random
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# In Memory class:
self.filename = os.path.join(BASE_DIR, "memory.json")

# In Values class:
self.filename = os.path.join(BASE_DIR, "values.json")

# ---------------- MEMORY ----------------

class Memory:
    def __init__(self, filename="memory.json"):
        self.filename = filename
        self.experiences = []
        self.stimulus_count = {}
        self.load()

    def store(self, experience):
        self.experiences.append(experience)

        s = experience["stimulus"]
        self.stimulus_count[s] = self.stimulus_count.get(s, 0) + 1

        self.save()

    def novelty(self, stimulus):
        count = self.stimulus_count.get(stimulus, 0)
        return 1 / (1 + count)

    def save(self):
        data = {
            "experiences": self.experiences,
            "stimulus_count": self.stimulus_count
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r") as f:
            data = json.load(f)
            self.experiences = data.get("experiences", [])
            self.stimulus_count = data.get("stimulus_count", {})

# ---------------- VALUE SYSTEM ----------------

class Values:
    def __init__(self, filename="values.json"):
        self.filename = filename
        self.state = 0.0
        self.load()

    def update(self, reward):
        self.state += reward
        self.state = max(-100, min(100, self.state))
        self.save()

    def mood(self):
        if self.state > 20:
            return "happy"
        elif self.state < -20:
            return "frustrated"
        return "neutral"

    def save(self):
        with open(self.filename, "w") as f:
            json.dump({"state": self.state}, f)

    def load(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r") as f:
            self.state = json.load(f).get("state", 0.0)

# ---------------- SENSORS ----------------

def sense_environment():
    # mock perception (replace later with camera, mic, etc.)
    return random.choice(["silence", "sound", "movement"])


# ---------------- ACTIONS ----------------

def choose_action(stimulus, mood):
    if stimulus == "sound":
        return "listen"
    if stimulus == "movement":
        return "look"
    return "wait"


def perform_action(action):
    print(f"Action: {action}")
    time.sleep(0.5)

# ---------------- AGENT ----------------

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.values = Values()

    def evaluate(self, stimulus, action):
        reward = 0.0

        if stimulus == "sound" and action == "listen":
            reward += 2
        if stimulus == "movement" and action == "look":
            reward += 2

        reward -= 0.3

        curiosity = self.memory.novelty(stimulus)
        reward += curiosity * 3

        return reward

    def step(self):
        stimulus = sense_environment()
        mood = self.values.mood()
        action = choose_action(stimulus, mood)

        novelty = self.memory.novelty(stimulus)
        reward = self.evaluate(stimulus, action)

        self.values.update(reward)

        self.memory.store({
            "stimulus": stimulus,
            "action": action,
            "reward": reward,
            "novelty": novelty,
            "value_state": self.values.state
        })

        print(f"Stimulus: {stimulus} | Mood: {mood} | Reward: {reward:.2f}")
        print(f"Novelty: {novelty:.2f}")

        perform_action(action)

# ---------------- MAIN LOOP ----------------

if __name__ == "__main__":
    agent = Agent()
    while True:
        agent.step()
        time.sleep(0.1)

