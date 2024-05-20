# Main File for stock/news correlation, the API Client and API and Webscraper Data is popualted here. 
# Imports 
import argparse
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import sys
import warnings
import yaml

from newsapi import NewsApiClient
from datetime import datetime, timedelta

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


def get_stock_data(api_cleint, ticker):

    keys=api_client.get_keylist()
    stock_key = keys['stockticker']
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={stock_key}'
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

def get_news(news_key, date_window):
    newsapi = NewsApiClient(news_key)

    # Define the time window
    #start_date = datetime.now() - timedelta(days=7)  # 7 days ago
    #end_date = datetime.now()  # Current date

    # Format the dates as strings
    #start_date_str = start_date.strftime('%Y-%m-%d')
    #end_date_str = end_date.strftime('%Y-%m-%d')
    start_date = datetime.strptime(date_window, '%Y-%m-%d')
    next_day = start_date + timedelta(days=2)
    print(str(start_date) + "|||||" + str(next_day))
    end_date=next_day

    # Query the News API for the top headlines in the specified time window
    top_headlines = newsapi.get_top_headlines(language='en', country='us')
    

    # Filter the top headlines based on criteria to approximate trending news stories
    trending_stories = []

    # Analyze the articles to determine trending stories
    for article in top_headlines['articles']:
        # You can define your own criteria for determining trending stories
        # For example, you can filter by popularity (e.g., number of shares, views, etc.)
        # Here, we'll consider articles published within the specified time window
        published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        if start_date <= published_at <= end_date:
            trending_stories.append(article)

    # Print the top headlines
    for article in top_headlines['articles']:
        print(article['title'])
        #print(article['description'])
        #print(article['url'])
        print() 
    return start_date, end_date, top_headlines


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
        data = get_stock_data(ticker)

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

    
    middle_index = len(dates) // 2
    print(dates[middle_index])
    key = api_client.get_keylist()
    print(key)
    newskey=key['worldnews']
    
    news_startdate, news_enddate, headlines = get_news(newskey, dates[middle_index])

    dates = pd.date_range(start=news_startdate, end=news_enddate)


    fig, ax = plt.subplots()
    ax.plot(dates, closing_prices, marker='o')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    for start_date, end_date in consecutive_lower_closes:
        news_titles = headlines
    
        # Find the midpoint date of the down days
        mid_date = pd.to_datetime(start_date) + (pd.to_datetime(end_date) - pd.to_datetime(start_date)) / 2
    
        # Find the corresponding y value (stock price) at the midpoint date
        mid_price = stock_prices[np.where(dates == mid_date)[0][0]]
    
        # Create a bubble with news titles
        news_text = '\n'.join(news_titles)
        annotation = TextArea(news_text, minimumdescent=False)
        bubble = AnnotationBbox(annotation, (mdates.date2num(mid_date), mid_price),
                            xybox=(50., 50.),
                            xycoords='data',
                            boxcoords="offset points",
                            arrowprops=dict(arrowstyle="->"))
        ax.add_artist(bubble)

    plt.legend()
    plt.show()





    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    plt.show()
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

    ticker, news, config, dummy = args
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

    args = parser.parse_args()
    args=([args.ticker, args.news, args.config, args.dummy])
    main(args)