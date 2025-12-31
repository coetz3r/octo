# action.py
import time

class Action:
    def __init__(self):
        self.last_action_time = time.time()

    def execute(self, thought):
        """
        Perform an action based on thought.
        """
        self.last_action_time = time.time()

        if "wonder" in thought.lower():
            self.speak(thought)
        else:
            self.idle()

    def speak(self, text):
        print(f"[manifess AI]: {text}")

    def idle(self):
        # intentionally imperfect silence
        pass
