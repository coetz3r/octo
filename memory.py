import json
import time
from pathlib import Path

class Memory:
    def __init__(self, path="data/memory.json", short_term_limit=20):
        self.path = Path(path)
        self.short_term_limit = short_term_limit
        self.short_term = []
        self.long_term = []

        self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path, "r") as f:
                self.long_term = json.load(f)
        else:
            self.long_term = []

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.long_term, f, indent=2)

    def remember(self, event, importance=0.5):
        memory_entry = {
            "time": time.time(),
            "event": event,
            "importance": importance
        }

        # short-term memory
        self.short_term.append(memory_entry)
        self.short_term = self.short_term[-self.short_term_limit:]

        # long-term memory (only important things)
        if importance >= 0.7:
            self.long_term.append(memory_entry)
            self._save()

    def recall_recent(self, n=5):
        return self.short_term[-n:]

    def recall_important(self, threshold=0.7):
        return [m for m in self.long_term if m["importance"] >= threshold]
