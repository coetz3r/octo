class InternalState:
    def __init__(self):
        self.energy = 1.0      # 0–1
        self.curiosity = 0.5   # 0–1
        self.mood = 0.0        # -1 to +1

    def update(self):
        # slow natural drift
        self.energy = max(0.0, self.energy - 0.001)
        self.curiosity = min(1.0, self.curiosity + 0.0005)

    def snapshot(self):
        return {
            "energy": round(self.energy, 3),
            "curiosity": round(self.curiosity, 3),
            "mood": round(self.mood, 3)
        }
