# main.py
from agent import Agent
from gui import ManifessGUI
import threading

agent = Agent()

# start agent loop in background
threading.Thread(target=agent.loop, daemon=True).start()

# start GUI (blocking)
gui = ManifessGUI(agent.gui_queue)
gui.run()

# stop agent when GUI closes
agent.stop()
