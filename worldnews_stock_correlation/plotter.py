import tkinter as tk
from tkinter import ttk, StringVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

# Function to update the plot
def update_plot():
    ticker = ticker_entry.get()
    keyword = keyword_var.get()
    
    # Generate sample data for plotting
    x = np.linspace(0, 10, 100)
    y = np.sin(x) + np.random.normal(0, 0.1, 100)
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(f"Plot for Ticker: {ticker} and Keyword: {keyword}")

    # Clear the old plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Add the new plot
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
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

# Create main window
root = tk.Tk()
root.title("Stock and Keyword Plotter")
root.geometry("800x600")

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create footer frame
footer_frame = tk.Frame(root)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create input fields and labels
ticker_label = tk.Label(footer_frame, text="Stock Ticker:")
ticker_label.pack(side=tk.LEFT, padx=(10, 2))
ticker_entry = tk.Entry(footer_frame)
ticker_entry.pack(side=tk.LEFT, padx=(0, 20))

keyword_label = tk.Label(footer_frame, text="Keyword:")
keyword_label.pack(side=tk.LEFT, padx=(10, 2))

# Create a dropdown menu for keywords
keywords = ["goober", "example1", "example2"]
keyword_var = StringVar(footer_frame)
keyword_var.set(keywords[0])
keyword_dropdown = ttk.Combobox(footer_frame, textvariable=keyword_var, values=keywords)
keyword_dropdown.pack(side=tk.LEFT, padx=(0, 20))

# Create submit button
submit_button = tk.Button(footer_frame, text="Submit", command=update_plot)
submit_button.pack(side=tk.LEFT, padx=(10, 10))

# Start the main loop
root.mainloop()