# agent.py
import time
import json
from queue import Queue

from memory import Memory
from state import InternalState
from perception import Perception
from action import Action

class Agent:
    def __init__(self, tick_rate=0.2):
        self.tick_rate = tick_rate
        self.running = False

        # Core systems
        self.memory = Memory()
        self.state = InternalState()
        self.perception = Perception()
        self.action = Action()

        # GUI communication
        self.gui_queue = Queue()

        # Load values
        self.values = self.load_values()

    # -----------------------------
    # Load values.json safely
    # -----------------------------
    def load_values(self):
        try:
            with open("values.json", "r") as f:
                return json.load(f)
        except Exception:
            # Default values if file missing
            return {
                "curiosity_threshold": 0.75,
                "memory_importance_base": 0.4,
                "memory_importance_curiosity_bonus": 0.4,
                "energy_decay": 0.001,
                "curiosity_growth": 0.0005,
                "silence_tolerance": 10.0
            }

    # -----------------------------
    # Core cognitive steps
    # -----------------------------
    def perceive(self):
        return self.perception.observe()

    def think(self, perception):
        """
        Generate a thought based on perception, memory, and state.
        """
        # Look at recent memory
        recent = self.memory.recall_recent(3)
        last_thought = None
        if recent:
            last_thought = recent[-1]["event"]["thought"]

        # 1 Curiosity-driven thought
        if self.state.curiosity > self.values.get("curiosity_threshold", 0.75):
            return "I wonder what this is."

        # 2 Continue pondering unresolved thought
        if last_thought and "wonder" in last_thought.lower():
            return "I am still thinking about that."

        # 3 Silence awareness
        if perception.get("idle_time", 0) > self.values.get("silence_tolerance", 10.0):
            return "It is very quiet."

        # 3 Default
        return "Nothing interesting is happening."

    def decide_importance(self, thought):
        importance = self.values.get("memory_importance_base", 0.4)
        if "wonder" in thought.lower():
            importance += self.values.get("memory_importance_curiosity_bonus", 0.4)
        return min(1.0, importance)

    def act(self, thought):
        self.action.execute(thought)
        state_snapshot = self.state.snapshot()
        self.gui_queue.put(f"THOUGHT: {thought}\nSTATE: {state_snapshot}")

    # -----------------------------
    # Main loop
    # -----------------------------
    def loop(self):
        self.running = True
        self.gui_queue.put("manifess AI started.")

        while self.running:
            perception = self.perceive()
            thought = self.think(perception)
            self.act(thought)

            # Remember event
            importance = self.decide_importance(thought)
            self.memory.remember(
                event={
                    "perception": perception,
                    "thought": thought,
                    "state": self.state.snapshot()
                },
                importance=importance
            )

            # Update internal state
            self.state.energy = max(0.0, self.state.energy - self.values.get("energy_decay", 0.001))
            self.state.curiosity = min(1.0, self.state.curiosity + self.values.get("curiosity_growth", 0.0005))

            time.sleep(self.tick_rate)

        self.gui_queue.put("manifess AI stopped.")

    def stop(self):
        self.running = False
