# perception.py
import time
import random

class Perception:
    def __init__(self):
        self.last_input_time = time.time()

    def observe(self):
        """
        Returns a perception dictionary.
        Simulates environment input.
        """
        now = time.time()
        idle_time = now - self.last_input_time

        # Generate stimulus
        if idle_time < 2:
            stimulus = random.choice(["background_noise", "movement_detected"])
        elif idle_time < 10:
            stimulus = "nothing"
        else:
            stimulus = "silence"

        return {
            "type": "environment",
            "idle_time": idle_time,
            "stimulus": stimulus
        }

    def external_input(self, text):
        """
        Call this when user or environment provides input.
        Resets idle time.
        """
        self.last_input_time = time.time()
        return {
            "type": "external",
            "content": text
        }
