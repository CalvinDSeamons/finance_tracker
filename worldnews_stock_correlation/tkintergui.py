# Main Tkinter script for launching the interactive GUI for the get_stock_info

import tkinter as tk
from tkinter import ttk

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class stocksleuth_gui:
    

    def __init__(self, root):
        self.root = root
        self.root.title("Stock Sleuth")
        self.root.geometry("400x300")
        # Initialize the GUI components
        self.setup_gui()

    def setup_gui(self):
        self.label1 = ttk.Label(self.root, text="Input 1:")
        self.label1.pack(pady=5)

        self.input1 = ttk.Entry(self.root)
        self.input1.pack(pady=5)

        # Create label and input field for the second input
        self.label2 = ttk.Label(self.root, text="Input 2:")
        self.label2.pack(pady=5)

        self.input2 = ttk.Entry(self.root)
        self.input2.pack(pady=5)

        self.submit_button = ttk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

        # Create the output field to show messages
        self.output_label = ttk.Label(self.root, text="", foreground="blue")
        self.output_label.pack(pady=10)

    def on_submit(self):
        # Get the values from the input fields
        self.var1 = self.input1.get()
        self.var2 = self.input2.get()

        # Show a message in the output field
        if self.var1 and self.var2:
            self.output_label.config(text="Submission successful!")
            print(f"Input 1: {self.var1}")
            print(f"Input 2: {self.var2}")
        else:
            self.output_label.config(text="Please fill in both input fields.", foreground="red")

    def on_button_click(self):
        self.label.config(text="Button Clicked!")

def launch_gui():
    root = tk.Tk()
    app = stocksleuth_gui(root)
    root.mainloop()