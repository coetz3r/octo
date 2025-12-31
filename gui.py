# gui.py
import tkinter as tk
import queue

class ManifessGUI:
    def __init__(self, data_queue):
        self.queue = data_queue

        self.root = tk.Tk()
        self.root.title("manifess AI")
        self.root.geometry("600x200")

        # Single Text widget for stable output
        self.text = tk.Text(self.root, state="disabled", wrap="word", height=8)
        self.text.pack(expand=True, fill="both", padx=10, pady=10)

        self.update_loop()

    def update_loop(self):
        """
        Update GUI once per 100ms, showing only latest thought/state.
        """
        if not self.queue.empty():
            message = self.queue.get()
            self._display(message)

        self.root.after(100, self.update_loop)

    def _display(self, text):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")  # clear old text
        self.text.insert("end", text)
        self.text.configure(state="disabled")

    def run(self):
        self.root.mainloop()
