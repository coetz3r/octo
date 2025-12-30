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
