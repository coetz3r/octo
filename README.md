# manifess AI
manifess AI is an experimental cognitive agent designed to demonstrate emergent behavior using simple rules, memory, perception, and internal state. It serves as a foundational platform for building AI-driven robotics or virtual agents with persistent memory and curiosity.

It is **optimized to run on a Raspberry Pi**, but can also run on other systems for development and testing.

## Features
- Persistent **short-term and long-term memory**
- Curiosity-driven thought generation
- Internal state tracking (energy, curiosity, mood)
- Perception of environment via simulated inputs
- GUI displays **thoughts, state, and actions** in real-time
- Actions executed directly through the GUI for simplicity
- Modular design suitable for experimentation and robotics integration

## Installation
1. Clone the repository:
```bash
git clone https://github.com/coetz3r/octo.git
cd manifess

2. (Optional) Create a Python virtual environment:
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3.Install required packages (if any):
pip install -r requirements.txt
The current code only uses Python standard libraries, so requirements.txt may not be necessary.

## Usage
Run the main program:
python3 main.py

- The AI agent starts in a background thread.
- The GUI shows thoughts, internal state, and actions in a single stable view.
- Close the GUI to stop the agent.
- Designed to run smoothly on Raspberry Pi, making it suitable for lightweight robotics projects.

## Quick Start Demo
Once you have installed and run `main.py`, you can observe the AI in action via the GUI.

1. Start the AI:

```bash
python3 main.py

2. Watch the GUI update in real-time:
- THOUGHT: Shows what the AI is thinking.
- STATE: Displays internal values like curiosity and energy.
- ACTION: Indicates what the AI is doing (exploring, waiting, idle).

# Example Behavior
* Curiosity-driven thought:
    THOUGHT: I wonder what this is.
    STATE: {'energy': 0.99, 'curiosity': 0.80}
    ACTION: explore
* Idle / waiting:
    THOUGHT: Nothing interesting is happening.
    STATE: {'energy': 0.98, 'curiosity': 0.81}
    ACTION: idle
* Silence detection (if no inputs for a while):
    THOUGHT: It is very quiet.
    STATE: {'energy': 0.97, 'curiosity': 0.82}
    ACTION: wait

# Interacting with the AI
- You can extend perception.py to add inputs (e.g., sensors, text commands).
- The GUI automatically updates thoughts and actions based on environmental stimuli and internal state.
- Adjust values.json to experiment with curiosity thresholds, energy decay, and memory importance.

The AI runs lightweight enough for a Raspberry Pi, so you can observe emergent behavior in real hardware without high resource usage.

## File Structure
manifess/
│
├── main.py           # Starts the agent loop and GUI
├── agent.py          # Core AI loop (perception, think, act, remember)
├── memory.py         # Short-term and long-term memory
├── perception.py     # Simulated environmental input
├── state.py          # Internal state tracking
├── gui.py            # Tkinter GUI, handles actions and displays
├── values.json       # Optional parameters (curiosity, memory importance, etc.)
└── README.md         # Project overview

## Customization
- values.json: Adjust thresholds for curiosity, memory importance, energy decay, and other parameters.
- Memory: Modify memory.py to change memory behavior or limits.
- Perception: Extend perception.py to incorporate real sensor inputs.
- Actions: Extend GUI methods (_explore(), _wait(), etc.) to link to robotics, motors, or other outputs.

## Contributing
We welcome contributions! You can help by:
- Reporting bugs or issues
- Suggesting new features or improvements
- Adding new perception modules or action methods
- Improving documentation or examples

## To contribute:
1. Fork the repository
2. Create a new branch (git checkout -b feature-name)
3. Make your changes and commit (git commit -m "Add feature")
4. Push to your branch (git push origin feature-name)
5. Open a Pull Request

Please keep contributions compatible with Raspberry Pi performance whenever possible.

## License

MIT License




------------------------------------------------------------------------------------
## Persistent State Files

This project uses simple JSON files to persist the agent’s internal state
between runs.

The following files are created automatically at runtime if they do not exist:

- `memory.json` – stores the agent’s experiences
- `values.json` – stores the agent’s internal value weights

These files are **not required to be downloaded or created manually**.
If they are missing, the agent will generate them on first launch.

If you want to reset the agent’s memory or values, simply delete these files
and restart the program.
