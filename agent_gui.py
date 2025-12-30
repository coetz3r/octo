import tkinter as tk
import threading
import time
from agent import Agent


class AgentGUI:
    def __init__(self, agent):
        self.agent = agent

        self.root = tk.Tk()
        self.root.title("Octo Cognition Monitor")

        #  Window size
        self.root.geometry("850x300")

        #  Main container (centering)
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True)

        self.labels = {}

        font = ("Courier", 12)

        for key in ["stimulus", "action", "reward", "head"]:
            lbl = tk.Label(
                self.container,
                text="",
                font=font,
                width=350,
                anchor="center",
                pady=5
            )
            lbl.pack()
            self.labels[key] = lbl

        self.update_gui()


    def update_gui(self):
        state = self.agent.state

        self.labels["stimulus"].config(text=f"Stimulus: {state['stimulus']}")
        self.labels["action"].config(text=f"Action: {state['action']}")
        self.labels["reward"].config(text=f"Reward: {state['reward']:.3f}")
        self.labels["head"].config(text=f"Head: x={state['head']['x']:.2f}, y={state['head']['y']:.2f}")

        self.root.after(200, self.update_gui)

    def run(self):
        self.root.mainloop()


def run_agent(agent):
    while True:
        agent.step()
        time.sleep(0.2)


if __name__ == "__main__":
    agent = Agent()

    threading.Thread(target=run_agent, args=(agent,), daemon=True).start()

    gui = AgentGUI(agent)
    gui.run()
