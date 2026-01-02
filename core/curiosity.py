# core/curiosity.py

class CuriosityEngine:
    def evaluate(self, event):
        """
        Returns a curiosity score 0.0 – 1.0
        """
        novelty = 0.0

        if isinstance(event, str):
            novelty = min(1.0, len(event) / 50.0)

        return novelty
