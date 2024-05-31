# Main Tkinter script for launching the interactive GUI for the get_stock_info

# Main Imports.
import json
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from tkinter import ttk, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class stocksleuth_gui:

    def __init__(self, root):
        self.root = root
        self.root.title("Stock and Keyword Plotter")
        self.root.geometry("800x600")

        # Create a frame for the plot
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create footer frame
        self.footer_frame = tk.Frame(self.root)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create input fields and labels
        self.ticker_label = tk.Label(self.footer_frame, text="Stock Ticker:")
        self.ticker_label.pack(side=tk.LEFT, padx=(10, 2))
        self.ticker_entry = tk.Entry(self.footer_frame)
        self.ticker_entry.pack(side=tk.LEFT, padx=(0, 20))

        self.keyword_label = tk.Label(self.footer_frame, text="Keyword:")
        self.keyword_label.pack(side=tk.LEFT, padx=(10, 2))

        # Create a dropdown menu for keywords
        self.keywords = ["goober", "example1", "example2"]
        self.keyword_var = StringVar(self.footer_frame)
        self.keyword_var.set(self.keywords[0])
        self.keyword_dropdown = ttk.Combobox(self.footer_frame, textvariable=self.keyword_var, values=self.keywords)
        self.keyword_dropdown.pack(side=tk.LEFT, padx=(0, 20))

        # Create submit button
        self.submit_button = tk.Button(self.footer_frame, text="Submit", command=self.test)
        self.submit_button.pack(side=tk.LEFT, padx=(10, 10))


    def update_plot(self):
        ticker = self.ticker_entry.get()
        keyword = self.keyword_var.get()

        # Generate sample data for plotting
        x = np.linspace(0, 10, 100)
        y = np.sin(x) + np.random.normal(0, 0.1, 100)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title(f"Plot for Ticker: {ticker} and Keyword: {keyword}")

        # Clear the old plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Add the new plot
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Enable scrolling and zooming
        def on_scroll(event):
            scale_factor = 1.1 if event.delta > 0 else 0.9
            ax.set_xlim([event.xdata - (event.xdata - ax.get_xlim()[0]) * scale_factor,
                         event.xdata + (ax.get_xlim()[1] - event.xdata) * scale_factor])
            ax.set_ylim([event.ydata - (event.ydata - ax.get_ylim()[0]) * scale_factor,
                         event.ydata + (ax.get_ylim()[1] - event.ydata) * scale_factor])
            canvas.draw()

        fig.canvas.mpl_connect('scroll_event', on_scroll)

def build_api_client(self):
        from get_stock_info import APIClient
        # This method takes the tkinter input fields values and builds the API client obejct from get_stock_info.py
        config='../configs/api-client.yaml' #This is sloppy but works for now.
        news = self.keywords
        webscraper=None
        dummy=True
        ticker=self.ticker_entry
        print(self.keywords)
        api_client = APIClient(config,ticker,dummy,news,webscraper)


def launch_gui():
    root = tk.Tk()
    app = stocksleuth_gui(root)
    root.mainloop()