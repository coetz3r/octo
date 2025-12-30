# agent_gui.py
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# In Memory class:
self.filename = os.path.join(BASE_DIR, "memory.json")

# In Values class:
self.filename = os.path.join(BASE_DIR, "values.json")


sys.path.append(os.path.join(os.path.dirname(__file__), '../core'))

from agent import Agent  # import your Agent class

class AgentGUI:
    def __init__(self, agent):
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("Agent Dashboard")

        # Labels
        self.mood_label = tk.Label(self.root, text="Mood: ")
        self.mood_label.pack()
        self.stimulus_label = tk.Label(self.root, text="Last Stimulus: ")
        self.stimulus_label.pack()
        self.action_label = tk.Label(self.root, text="Last Action: ")
        self.action_label.pack()
        self.novelty_label = tk.Label(self.root, text="Novelty: ")
        self.novelty_label.pack()
        self.memory_label = tk.Label(self.root, text="Memory Size: ")
        self.memory_label.pack()

        # Action log
        self.log_box = scrolledtext.ScrolledText(self.root, width=50, height=10)
        self.log_box.pack()
        self.log_box.configure(state='disabled')

        # Start agent loop in a separate thread
        threading.Thread(target=self.run_agent_loop, daemon=True).start()

        self.root.mainloop()

    def run_agent_loop(self):
        while True:
            self.agent.step()
            self.update_gui()
            time.sleep(0.1)  # adjust loop speed

    def update_gui(self):
        latest = self.agent.memory.experiences[-1] if self.agent.memory.experiences else {}
        mood = self.agent.values.mood()
        stimulus = latest.get("stimulus", "N/A")
        action = latest.get("action", "N/A")
        novelty = latest.get("novelty", 0)
        memory_size = len(self.agent.memory.experiences)

        self.mood_label.config(text=f"Mood: {mood}")
        self.stimulus_label.config(text=f"Last Stimulus: {stimulus}")
        self.action_label.config(text=f"Last Action: {action}")
        self.novelty_label.config(text=f"Novelty: {novelty:.2f}")
        self.memory_label.config(text=f"Memory Size: {memory_size}")

        # Update log
        self.log_box.configure(state='normal')
        self.log_box.insert(tk.END, f"{stimulus} -> {action} (Novelty: {novelty:.2f})\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state='disabled')

if __name__ == "__main__":
    agent = Agent()
    gui = AgentGUI(agent)
