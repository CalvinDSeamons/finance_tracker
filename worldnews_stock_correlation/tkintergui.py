# Main Tkinter script for launching the interactive GUI for the get_stock_info

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class stocksleuth_gui(tk.Tk):
    

    def __init__(self):
        super().__init__()
        self.title("StockSleuth")
        self.geometry("800x600")
        self.configure(bg='gray')

        # Input frame
        self.input_frame = ttk.Frame(self, width=800, height=100)
        self.input_frame.pack(side=tk.TOP, fill=tk.X)

        # Label and input field
        self.label = ttk.Label(self.input_frame, text="Enter Stock Symbol:")
        self.label.pack(side=tk.LEFT, padx=10, pady=10)

        self.input_field = ttk.Entry(self.input_frame, width=20)
        self.input_field.pack(side=tk.LEFT, padx=10, pady=10)

        # Submit button
        self.submit_button = ttk.Button(self.input_frame, text="Submit", command=self.fetch_and_plot_data)
        self.submit_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Plot frame
        self.plot_frame = ttk.Frame(self, width=800, height=500)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def fetch_and_plot_data(self):
        # Simulating fetching JSON data (you can replace this with actual API calls)
        stock_symbol = self.input_field.get()
        with open('../dummy_data/AAPL.json', 'r') as file:
                data = json.load(file)
       
        
        dates = []
        close_prices = []
        
        for date, values in data["Time Series (Daily)"].items():
            dates.append(date)
            close_prices.append(float(values["4. close"]))

        self.plot_data(dates, close_prices)

    def plot_data(self, dates, close_prices):
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, close_prices, marker='o')
        ax.set_title("Stock Prices Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price")
        ax.grid(True)
        
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Add new plot
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



def launch_gui():
    root = tk.Tk()
    app = stocksleuth_gui()
    root.mainloop()