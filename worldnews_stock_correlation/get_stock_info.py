# Main File for stock/news correlation, the API Client and API and Webscraper Data is popualted here. 
# Imports 
import argparse
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import requests
import sys
import warnings
import yaml

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from newsapi import NewsApiClient
import matplotlib.cbook as cbook
from matplotlib.offsetbox import AnnotationBbox, TextArea



class APIClient:
    # APIClient contains the argparser data, api keys, as well as unique functions for plotting data. 

    def __init__(self,config_file, ticker, dummy, news=None):
        # Setting arpparser args such as ticker and news keywords.
        self.ticker = ticker
        self.news = news
        self.dummy = dummy
        # Loading in and setting all API Keys from config file.
        self.config = self.load_config(config_file)
        self.news_api_key = self.config['keys']['world_news_api_key']
        self.stock_api_key = self.config['keys']['stock_data_api_key']
        self.reddit_api_key = self.config['keys']['reddit_data_api_key']
        self.fb_api_key = self.config['keys']['facebook_data_api_key']
        self.instagram_api_key = self.config['keys']['instagram_data_api_key']


    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    
    def test(self):
        # This is just here for my sanity.
        print("Hello from the API Client!")

    def get_ticker(self):
        # Returns the stock ticker name.
        return self.ticker
    
    def get_news_keywords(self):
        # Returns the keywords for news articles to search.
        return self.news

    def get_dummy(self):
        # Return T or F depending on argparse flag.
        return self.dummy
    
    def get_keylist(self):
        self.keylist = {}
        self.keylist['worldnews']=self.news_api_key
        self.keylist['stockticker']=self.stock_api_key
        return self.keylist
    
# --------------End of API Client Class---------------    


def error_exit(message, exit_code=1):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


def get_stock_data(api_client):

    keys=api_client.get_keylist()
    stock_key = keys['stockticker']
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={api_client.get_ticker()}&apikey={stock_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'Error Message' in data:
            error_message = "Check to make sure your Ticker is valid and your apikey is correct"
            print(f"Error: {error_message}")
            quit()
        else:
            # Process the data
            print(data)
    else:
        print("Error: Failed to fetch data from Alpha Vantage API")
        
    return data

def get_news_data():
    #bleh bleh news idk
    BASE_URL     = 'https://newsapi.org/v2/'
    endpoint     = 'everything'
    params       = {
                    'q': 'your query here',
                    'apiKey': news_api_key,
                   }
    
    response = requests.get(BASE_URL + endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
    
        for article in articles:
            print(article['title'])
            print(article['description'])
            print(article['url'])
            print('---')
    else:
        print('Error:', response.status_code)

def get_news(news_key, beginning_date, ending_date):
    newsapi = NewsApiClient(news_key)

    # Define the time window
    #start_date = datetime.now() - timedelta(days=7)  # 7 days ago
    #end_date = datetime.now()  # Current date

    # Format the dates as strings
    #start_date_str = start_date.strftime('%Y-%m-%d')
    #end_date_str = end_date.strftime('%Y-%m-%d')
    #start_date = datetime.strptime(beginning_date, '%Y-%m-%d')
    #end_date = datetime.strptime(ending_date, '%Y-%m-%d')

    end_date = datetime.now()
    start_date = end_date - relativedelta(months=1)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    #print(str(start_date) + "|||||" + str(end_date))
   

    # Query the News API for the top headlines in the specified time window
    #top_headlines = newsapi.get_top_headlines(language='en', country='us')
    top_headlines = newsapi.get_everything(
    q='stock',
    from_param=start_date_str,
    to=end_date_str,
    language='en',
    sort_by='publishedAt',
    page=1)


    # Filter the top headlines based on criteria to approximate trending news stories
    trending_stories = {}

    # Analyze the articles to determine trending stories
    for article in top_headlines['articles']:
        # You can define your own criteria for determining trending stories
        # For example, you can filter by popularity (e.g., number of shares, views, etc.)
        # Here, we'll consider articles published within the specified time window
        published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        published_date = published_at.date()
        if start_date <= published_at <= end_date:
            trending_stories[article['title']]=published_at.date()

    # Print the top headlines
    for article in top_headlines['articles']:
        published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        published_date = published_at.date()
        #print(article['title']+ "-----"+str(published_at))
        #print(article['description'])
        #print(article['url'])
        #print(published_date)
        trending_stories[article['title']]=published_at.date()
    #print(trending_stories)
    return trending_stories

def plotstock(api_client):

    ticker=api_client.get_ticker()

    if api_client.get_dummy():
        if ticker == 'NVDA':
            with open('../dummy_data/NVDA.json', 'r') as file:
                data = json.load(file)
        elif ticker == 'AAPL':
            with open('../dummy_data/AAPL.json', 'r') as file:
                data = json.load(file)
        else:
            print("Error: When using dummy flag specify wither NVDA or AAPL as the ticker.")
            quit()
    else:
        data = get_stock_data(api_client)

    dates = []
    closing_prices = []

    dates = list(data['Time Series (Daily)'].keys())[::-1]  # Reverse the order to plot from oldest to newest
    closing_prices = [float(data['Time Series (Daily)'][date]['4. close']) for date in dates]
    symbol = data['Meta Data']['2. Symbol']

    #This method needs to be moved elsewhere
    consecutive_lower_closes = []
    consecutive_count = 0
    for i in range(1, len(closing_prices)):
        if closing_prices[i] < closing_prices[i - 1]:
            consecutive_count += 1
        else:
            if consecutive_count >= 5:
                consecutive_lower_closes.extend(range(i - consecutive_count - 1, i))
            consecutive_count = 0

    
    
    key = api_client.get_keylist()
    print(key)
    newskey=key['worldnews']
    
    newslist = get_news(newskey, dates[0], dates[len(dates)-1])

    dates = []
    close_prices = []

    for date_str, daily_data in data["Time Series (Daily)"].items():
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        close_price = float(daily_data["4. close"])
        dates.append(date)
        close_prices.append(close_price)

    # Prepare the news data
    news_dates = set(newslist.values())
    news_annotations = {date: [] for date in news_dates}
    for title, date in newslist.items():
        news_annotations[date].append(title)

    # Create the plot
    fig, ax = plt.subplots()

    # Plot the stock closing prices
    ax.plot(dates, close_prices, marker='o', linestyle='-', color='b', label='Closing Prices')

    # Highlight dates with news articles
    news_bubbles = [date for date in dates if date in news_dates]
    news_prices = [close_prices[dates.index(date)] for date in news_bubbles]

    # Plot the news bubbles
    bubble_plot = ax.scatter(news_bubbles, news_prices, color='red', s=100, label='News Articles')

    # Function to handle click events
    def onpick(event):
        if event.artist != bubble_plot:
            return
        ind = event.ind[0]
        date_clicked = news_bubbles[ind]
        titles = news_annotations[date_clicked]
        news_text = "\n".join(titles)
        print(f"News on {date_clicked}:\n{news_text}")

    # Connect the click event to the handler function
    fig.canvas.mpl_connect('pick_event', onpick)

    # Annotate the news bubbles
    for date, price in zip(news_bubbles, news_prices):
        annotation_text = "\n".join(news_annotations[date])
        annotation = AnnotationBbox(TextArea(annotation_text), (mdates.date2num(date), price),
                                    xybox=(30, 30),
                                    xycoords='data',
                                    boxcoords="offset points",
                                    arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        annotation.set_visible(False)
        ax.add_artist(annotation)
        def on_hover(event):
            if event.artist == bubble_plot:
                ind = event.ind[0]
                annotation.set_visible(True)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_hover)

    # Format the x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')
    ax.set_title('Stock Closing Prices with News Overlays')
    ax.legend()

    plt.show()

    #plt.show()
    # ----------- Old MatPlotLib Method -----------#
    #plt.figure(figsize=(16, 8))
    #plt.plot(dates, closing_prices, marker='o', linestyle='-')

    #plt.scatter([dates[i] for i in consecutive_lower_closes], 
    #        [closing_prices[i] for i in consecutive_lower_closes], 
    #        color='red', zorder=5, label='Consecutive Lower Closes')

    #plt.title(symbol+' Closing Prices')
    #plt.xlabel('Date',rotation=135)
    #plt.ylabel('Closing Price ($)')
    #plt.tight_layout()
    #plt.show()

def main(args):
    # Main method creates the api_client objects and kicks off argparse actions.

    ticker, news, config, dummy, gui, webscraper = args
    api_client = APIClient(config, ticker, dummy, news)

    api_client.test()
    api_client.get_ticker()
    api_client.get_news_keywords()

    plotstock(api_client)
    



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Command line inputs for stockapp")

    parser.add_argument("--ticker", "-t", type=str, help="Stock Market Ticker, This value is required. Usage: --ticker=AAPL",required=True)
    parser.add_argument("--news",   "-n", nargs='*', type=str, help="Keywords to associate to online news. Usage: --news=Biden,apple,Gaza,Planecrash")
    parser.add_argument("--config", "-c", help="Yaml Configuration file containing the api keys. "
                                               "This will override default config. Usage: --config='path_to_your_config"
                                               , default='../configs/worldnews_stock__correlation.yaml')
    parser.add_argument("--dummy",  "-d", action='store_true', help="If APIs request limit has been reached dummy will use saved static data. "
                                                                     "Usage: -d or --dummy")
    parser.add_argument("--gui", "-g", action='store_true', help="Launches a user GUI, flags such as ticker, and news will be overridden. "
                                                                  "Usage: -g ot --gui")
    parser.add_argument("--webscraper","-ws", nargs='*', type=str, help="Keywords to associte to online news, using webscraping instead of apis, slower but more data. "
                                                                        "Usage: --webscraper=Turtle, tree, plane" )

    args = parser.parse_args()
    args=([args.ticker, args.news, args.config, args.dummy, args.gui, args.webscraper])
    main(args)