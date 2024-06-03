# Main Tkinter script for launching the interactive GUI for the get_stock_info

# Main Imports.
import json
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from tkinter import ttk, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import get_stock_info


class stocksleuth_gui:

    def __init__(self, root):

        # The init functions contains all the code for building the tkinter frames.
        # It's a hot mess but doesn't need to be touched much.
        # -------------------------------------------------- #

        self.root = root
        self.root.title("Stock and Keyword Plotter")
        self.root.geometry("800x600")

        # Create a frame for the plot
        self.plot_frame = tk.Frame(self.root, bg="#a9a9a9")
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create footer frame with a darker gray background
        self.footer_frame = tk.Frame(self.root)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure grid layout for the footer frame
        self.footer_frame.columnconfigure(0, weight=1)
        self.footer_frame.columnconfigure(1, weight=1)
        self.footer_frame.columnconfigure(2, weight=1)
        self.footer_frame.columnconfigure(3, weight=1)
        self.footer_frame.columnconfigure(4, weight=1)
        self.footer_frame.columnconfigure(5, weight=1)
        self.footer_frame.columnconfigure(6, weight=1)
        self.footer_frame.columnconfigure(7, weight=1)
        self.footer_frame.columnconfigure(8, weight=1)

        # Create input fields and labels
        self.ticker_label = tk.Label(self.footer_frame, text="Stock Ticker:")
        self.ticker_label.grid(row=0, column=0, padx=(10, 2), pady=5, sticky='w')
        self.ticker_entry = tk.Entry(self.footer_frame)
        self.ticker_entry.grid(row=0, column=1, padx=(0, 20), pady=5, sticky='w')

        self.keyword_label = tk.Label(self.footer_frame, text="Keyword:")
        self.keyword_label.grid(row=0, column=2, padx=(10, 2), pady=5, sticky='w')

        # Create a dropdown menu for keywords
        self.keywords = ["goober", "example1", "example2"]
        self.keyword_var = StringVar(self.footer_frame)
        self.keyword_var.set(self.keywords[0])
        self.keyword_dropdown = ttk.Combobox(self.footer_frame, textvariable=self.keyword_var, values=self.keywords)
        self.keyword_dropdown.grid(row=0, column=3, padx=(0, 20), pady=5, sticky='w')

        # Create submit button
        self.submit_button = tk.Button(self.footer_frame, text="Submit", command=self.build_api_client)
        self.submit_button.grid(row=0, column=4, padx=(10, 10), pady=5, sticky='w')

        # Create print button
        self.print_button = tk.Button(self.footer_frame, text="Create Obj.", command=self.display_obj)
        self.print_button.grid(row=0, column=5, padx=(10, 10), pady=5, sticky='w')

        # Define variables for toggle switches
        self.reddit_var = tk.BooleanVar(value=False)
        self.dummy_data_var = tk.BooleanVar(value=False)
        self.newsapi_var = tk.BooleanVar(value=False)
        self.facebook_var = tk.BooleanVar(value=False)
        self.instagram_var = tk.BooleanVar(value=False)
        # Create toggle switches and labels
        self.reddit_label = tk.Label(self.footer_frame, text="Reddit:")
        self.reddit_label.grid(row=1, column=0, padx=(10, 2), pady=5, sticky='w')
        self.reddit_toggle = ttk.Checkbutton(self.footer_frame, variable=self.reddit_var, onvalue=True, offvalue=False)
        self.reddit_toggle.grid(row=1, column=1, padx=(0, 20), pady=5, sticky='w')

        self.dummy_data_label = tk.Label(self.footer_frame, text="Dummy Data:")
        self.dummy_data_label.grid(row=1, column=2, padx=(10, 2), pady=5, sticky='w')
        self.dummy_data_toggle = ttk.Checkbutton(self.footer_frame, variable=self.dummy_data_var, onvalue=True, offvalue=False)
        self.dummy_data_toggle.grid(row=1, column=3, padx=(0, 20), pady=5, sticky='w')

        self.newsapi_label = tk.Label(self.footer_frame, text="NewsAPI:")
        self.newsapi_label.grid(row=1, column=4, padx=(10, 2), pady=5, sticky='w')
        self.newsapi_toggle = ttk.Checkbutton(self.footer_frame, variable=self.newsapi_var, onvalue=True, offvalue=False)
        self.newsapi_toggle.grid(row=1, column=5, padx=(0, 20), pady=5, sticky='w')

        self.newsapi_label = tk.Label(self.footer_frame, text="Instagram:")
        self.newsapi_label.grid(row=2, column=0, padx=(10, 2), pady=5, sticky='w')
        self.newsapi_toggle = ttk.Checkbutton(self.footer_frame, variable=self.instagram_var, onvalue=True, offvalue=False)
        self.newsapi_toggle.grid(row=2, column=1, padx=(0, 20), pady=5, sticky='w')

        self.newsapi_label = tk.Label(self.footer_frame, text="Facebook:")
        self.newsapi_label.grid(row=2, column=2, padx=(10, 2), pady=5, sticky='w')
        self.newsapi_toggle = ttk.Checkbutton(self.footer_frame, variable=self.facebook_var, onvalue=True, offvalue=False)
        self.newsapi_toggle.grid(row=2, column=3, padx=(0, 20), pady=5, sticky='w')



    def build_api_client(self):
         # This method takes inputs saved via the buttons and returns it for the creation of the apiclient for data access.
         ticker = self.ticker_entry.get()
         keywords= self.keyword_var.get()
         config='../configs/api-client.yaml'
         webscraper=None
         dummy = self.dummy_data_var.get()
         self.api_client = get_stock_info.APIClient(config,ticker,dummy,keywords,webscraper) # creates api_cleint obj within tkinter.


    def display_obj(self):
         print(self.api_client.get_news_keywords())


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