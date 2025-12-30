import os
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
from agent import Agent

# -------------------
# GUI class
# -------------------
class AgentGUI:
    def __init__(self, agent):
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("Agent Dashboard")

        # Labels
        self.mood_label = tk.Label(self.root, text="Mood: 0")
        self.mood_label.pack()

        self.stimulus_label = tk.Label(self.root, text="Stimulus: ")
        self.stimulus_label.pack()

        self.action_label = tk.Label(self.root, text="Action: ")
        self.action_label.pack()

        self.novelty_label = tk.Label(self.root, text="Novelty: ")
        self.novelty_label.pack()

        # Scrolled log
        self.log = scrolledtext.ScrolledText(self.root, width=50, height=15)
        self.log.pack()

        # Start agent loop in background
        threading.Thread(target=self.run_agent_loop, daemon=True).start()
        self.root.mainloop()

    def run_agent_loop(self):
        while True:
            stimulus = self.agent.perceive()
            action = self.agent.decide(stimulus)
            self.agent.act(action)
            reward = self.agent.reward(stimulus)
            self.agent.values.update(reward)
            novelty = self.agent.memory.novelty(stimulus)
            self.agent.memory.store(stimulus)

            # Update GUI
            self.mood_label.config(text=f"Mood: {sum(self.agent.values.data.values()):.2f}")
            self.stimulus_label.config(text=f"Stimulus: {stimulus}")
            self.action_label.config(text=f"Action: {action}")
            self.novelty_label.config(text=f"Novelty: {novelty:.2f}")

            self.log.insert(tk.END, f"Stimulus: {stimulus}, Action: {action}, Novelty: {novelty:.2f}\n")
            self.log.see(tk.END)

            time.sleep(0.5)  # adjust speed

# -------------------
# Run GUI
# -------------------
if __name__ == "__main__":
    agent = Agent()
    gui = AgentGUI(agent)
