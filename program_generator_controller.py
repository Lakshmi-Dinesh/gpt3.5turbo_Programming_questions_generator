"""
@author: Lakshmi Dinesh
The Engine and GUI are initialized here
"""

import tkinter as t
from tkinter import messagebox as mb
from program_generator_ui import ProgramGeneratorGUI
from program_generator_engine import ProgramGeneratorEngine

# Initialize the backend
engine = ProgramGeneratorEngine()

# Train the GPT engine with initial system, user data and model responses
trained = engine.train_engine()
if not trained:
    mb.showerror("Error", "Cannot communicate with OpenAI!\nCheck your connection and try again later!")

# Launch GUI, pass engine object and wait for user input
window = t.Tk()
ProgramGeneratorGUI(window, engine)
window.mainloop()
