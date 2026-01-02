# core/state.py

class InternalState:
    def __init__(self):
        # core scalar values
        self.energy = 0.5      # 0.0 – 1.0
        self.mood = 0.0        # -1.0 – 1.0
        self.curiosity = 0.5   # 0.0 – 1.0

    def apply_delta(self, energy=0.0, mood=0.0, curiosity=0.0):
        self.energy = max(0.0, min(1.0, self.energy + energy))
        self.curiosity = max(0.0, min(1.0, self.curiosity + curiosity))
        self.mood = max(-1.0, min(1.0, self.mood + mood))

    def snapshot(self):
        return {
            "energy": round(self.energy, 3),
            "mood": round(self.mood, 3),
            "curiosity": round(self.curiosity, 3),
        }
