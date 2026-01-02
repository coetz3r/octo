# agent/cognition.py

from core.state import InternalState
from core.memory import MemoryStore
from core.curiosity import CuriosityEngine

class Cognition:
    def __init__(self):
        self.state = InternalState()
        self.memory = MemoryStore()
        self.curiosity = CuriosityEngine()

    def observe(self, event):
        curiosity_score = self.curiosity.evaluate(event)

        # update internal chemistry
        self.state.apply_delta(
            curiosity=curiosity_score * 0.1,
            mood=curiosity_score * 0.05,
            energy=-0.02
        )

        # store memory if meaningful
        if curiosity_score > 0.2:
            self.memory.add(
                content=event,
                value=curiosity_score
            )

        return curiosity_score
