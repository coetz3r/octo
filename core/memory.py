# core/memory.py
import time
import uuid

class Memory:
    def __init__(self, content, value):
        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.content = content
        self.value = value  # importance / emotional weight

class MemoryStore:
    def __init__(self, max_size=200):
        self.memories = []
        self.max_size = max_size

    def add(self, content, value):
        mem = Memory(content, value)
        self.memories.append(mem)

        # prune weakest memories
        if len(self.memories) > self.max_size:
            self.memories.sort(key=lambda m: abs(m.value), reverse=True)
            self.memories = self.memories[: self.max_size]

    def recent(self, n=5):
        return self.memories[-n:]

    def strongest(self, n=5):
        return sorted(self.memories, key=lambda m: abs(m.value), reverse=True)[:n]
