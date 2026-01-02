import tkinter as tk
import threading
import time
from agent import Agent


class AgentGUI:
    def __init__(self, agent):
        self.agent = agent

        self.root = tk.Tk()
        self.root.title("Octo Cognition Monitor")

        # Window size
        self.root.geometry("850x350")

        # Main container (centering)
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True)

        self.labels = {}

        font = ("Courier", 12)

        # Main info labels
        for key in ["stimulus", "action", "reward", "head"]:
            lbl = tk.Label(
                self.container,
                text="",
                font=font,
                width=60,
                anchor="w",
                pady=5
            )
            lbl.pack()
            self.labels[key] = lbl

        # Introspection label
        self.mind_label = tk.Label(
            self.container,
            text="",
            font=font,
            justify="left",
            anchor="w",
            pady=5
        )
        self.mind_label.pack(pady=10)

        # Start GUI updates
        self.update_gui()

    def update_gui(self):
        state = self.agent.state.snapshot()  # get current state dict

        # Safe access using .get() with defaults
        self.labels["stimulus"].config(
            text=f"Energy: {state.get('energy', 0):.2f}, Curiosity: {state.get('curiosity', 0):.2f}"
        )
        self.labels["action"].config(
            text=f"Action: {state.get('action', 'TBD')}"
        )
        self.labels["reward"].config(
            text=f"Reward: {state.get('reward', 0.0):.2f}"
        )

        head = state.get('head', {'x': 0.0, 'y': 0.0})
        self.labels["head"].config(
            text=f"Head: x={head.get('x', 0.0):.2f}, y={head.get('y', 0.0):.2f}"
        )

        # Introspection display (from last_introspection dict)
        if self.agent.last_introspection:
            info = self.agent.last_introspection
            mind_text = (
                f"Drive: {info.get('dominant_drive', 'N/A')}\n"
                f"Energy: {info.get('energy', 0.0):.2f}\n"
                f"Curiosity: {info.get('curiosity', 0.0):.2f}\n"
                f"Mood: {info.get('mood', 0.0):.2f}\n\n"
                f"Why:\n{info.get('notes', '')}"
            )
            self.mind_label.config(text=mind_text)
        else:
            self.mind_label.config(text="Introspection: N/A")

        # Schedule next GUI update
        self.root.after(200, self.update_gui)

    def run(self):
        self.root.mainloop()


def run_agent(agent):
    while True:
        agent.step()
        time.sleep(agent.tick_rate)


if __name__ == "__main__":
    agent = Agent()

    # Start agent loop in a background thread
    threading.Thread(target=run_agent, args=(agent,), daemon=True).start()

    # Start GUI
    gui = AgentGUI(agent)
    gui.run()
