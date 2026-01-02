# introspection.py

class Introspection:
    def __init__(self):
        self.last_report = {}

    def reflect(self, state, perception, thought, memory=None):
        """
        Observe internal processes and explain them.
        """
        report = {
            "energy": state.energy,
            "curiosity": state.curiosity,
            "mood": state.mood,
            "perceived": perception,
            "current_thought": thought,
            "dominant_drive": self._dominant_drive(state),
            "notes": self._explain(state, perception, thought)
        }

        self.last_report = report
        return report

    def _dominant_drive(self, state):
        if state.energy < 0.3:
            return "rest"
        if state.curiosity > 0.6:
            return "explore"
        return "idle"

    def _explain(self, state, perception, thought):
        if state.curiosity > state.energy:
            return "Curiosity outweighed energy conservation."
        if state.energy < 0.3:
            return "Low energy limited action."
        return "No strong internal conflict detected."
