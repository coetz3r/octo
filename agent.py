import random
import time


# -----------------------------
# Memory System
# -----------------------------
class Memory:
    def __init__(self):
        self.experiences = []      # list of dicts
        self.values = {}           # action:value memory

    def store(self, experience):
        # experience MUST be a dict
        self.experiences.append(experience)

    def novelty(self, stimulus_type):
        count = sum(
            1 for e in self.experiences
            if e.get("stimulus_type") == stimulus_type
        )
        return 1.0 / (1 + count)

    def update_value(self, key, reward, alpha=0.2):
        old = self.values.get(key, 0.0)
        new = old + alpha * (reward - old)
        self.values[key] = new

    def get_value(self, key):
        return self.values.get(key, 0.0)


# -----------------------------
# Agent
# -----------------------------
class Agent:
    def __init__(self):
        self.memory = Memory()

        # head orientation (normalized)
        self.head_x = 0.5  # yaw
        self.head_y = 0.5  # pitch

        self.actions = [
            "look_left",
            "look_right",
            "look_up",
            "look_down",
            "wait"
        ]

    # -------------------------
    # Perception (simulation)
    # -------------------------
    def perceive(self):
        """
        Simulated stimulus.
        Replace later with real vision / audio.
        """
        return {
            "type": random.choice(["light", "sound", "movement"]),
            "x": random.random(),
            "y": random.random()
        }

    # -------------------------
    # Appraisal
    # -------------------------
    def appraise(self, stimulus):
        novelty = self.memory.novelty(stimulus["type"])

        dx = abs(stimulus["x"] - self.head_x)
        dy = abs(stimulus["y"] - self.head_y)
        distance = dx + dy

        salience = 1.0 - distance
        salience = max(0.0, salience)

        return {
            "novelty": novelty,
            "salience": salience
        }

    # -------------------------
    # Decision
    # -------------------------
    def choose_action(self, stimulus, appraisal):
        # exploration
        if random.random() < appraisal["novelty"]:
            return random.choice(self.actions)

        # exploitation
        scored = []
        for action in self.actions:
            key = f"{action}:{stimulus['type']}"
            value = self.memory.get_value(key)
            scored.append((value, action))

        scored.sort(reverse=True)
        return scored[0][1]

    # -------------------------
    # Action (Head Movement)
    # -------------------------
    def perform_action(self, action, stimulus):
        step = 0.1

        if action == "look_left":
            self.head_x -= step
        elif action == "look_right":
            self.head_x += step
        elif action == "look_up":
            self.head_y -= step
        elif action == "look_down":
            self.head_y += step
        elif action == "wait":
            pass

        # clamp head movement
        self.head_x = min(max(self.head_x, 0.0), 1.0)
        self.head_y = min(max(self.head_y, 0.0), 1.0)

        return self.compute_reward(stimulus)

    # -------------------------
    # Reward Function
    # -------------------------
    def compute_reward(self, stimulus):
        dx = abs(stimulus["x"] - self.head_x)
        dy = abs(stimulus["y"] - self.head_y)

        distance = dx + dy
        reward = 1.0 - distance

        return max(0.0, reward)

    # -------------------------
    # Learning Loop
    # -------------------------
    def step(self):
        stimulus = self.perceive()
        appraisal = self.appraise(stimulus)
        action = self.choose_action(stimulus, appraisal)
        reward = self.perform_action(action, stimulus)

        key = f"{action}:{stimulus['type']}"
        self.memory.update_value(key, reward)

        self.memory.store({
            "stimulus_type": stimulus["type"],
            "action": action,
            "reward": reward,
            "head_x": self.head_x,
            "head_y": self.head_y
        })

        return {
            "stimulus": stimulus,
            "action": action,
            "reward": reward,
            "head": (self.head_x, self.head_y)
        }


# -----------------------------
# Standalone test loop
# -----------------------------
if __name__ == "__main__":
    agent = Agent()

    for i in range(50):
        result = agent.step()
        print(
            f"{i:03d} | "
            f"stimulus={result['stimulus']['type']} "
            f"action={result['action']} "
            f"reward={result['reward']:.3f} "
            f"head={result['head']}"
        )
        time.sleep(0.1)
