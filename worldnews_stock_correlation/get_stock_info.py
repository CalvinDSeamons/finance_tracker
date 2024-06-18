# Main File for stock/news correlation, the API Client and API and Webscraper Data is popualted here. 
# Imports 
import argparse
import json
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import praw
import re
import requests
import sys
import time
import warnings
import yaml

from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from newsapi import NewsApiClient
from matplotlib.offsetbox import AnnotationBbox, TextArea
from psaw import PushshiftAPI

#Imports for other scripts in the stocksleuth app.
from tkintergui import launch_gui


class APIClient:
    # APIClient contains the argparser data, api keys, as well as unique functions for plotting data. 

    def __init__(self,config_file, ticker, dummy, news=None, webscraper=None):
        # Setting arpparser args such as ticker and news keywords.
        self.ticker     = ticker
        self.news       = news
        self.dummy      = dummy
        self.webscraper = webscraper
        # Loading in and setting all API Keys from config file.
        self.config            = self.load_config(config_file)
        self.news_api_key      = self.config['keys']['world_news_api_key']
        self.stock_api_key     = self.config['keys']['stock_data_api_key']
        self.reddit_api_key    = self.config['keys']['reddit_data_api_key']
        self.fb_api_key        = self.config['keys']['facebook_data_api_key']
        self.instagram_api_key = self.config['keys']['instagram_data_api_key']
        # Loading in Reddit Configs.
        self.client_id     = self.config['reddit']['client_id']
        self.client_secret = self.config['reddit']['client_secret']
        self.user_agent    = self.config['reddit']['user_agent']


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
        # Returns a full list of API keys from the config.
        self.keylist = {}
        self.keylist['worldnews']=self.news_api_key
        self.keylist['stockticker']=self.stock_api_key
        return self.keylist
    
    def get_stock_api(self):
        # Returns Stock API Key.
        return self.stock_api_key
    
    def get_news_api(self):
        # Returns News API Key.
        return self.news_api_key
    
    def get_reddit_api_client(self):
        # To cut down on redudant code this creates the Reddit PRAW endpoint and returns it. 
        self.reddit = praw.Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        user_agent=self.user_agent
        )
        return self.reddit
        
    
# --------------End of API Client Class---------------    


def error_exit(message, exit_code=1):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


def get_stock_data(api_client):
    #print("#"*25)
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
        print("Error: Failed to fetch data from Alpha Vantage API")
    #print(data)  
    return data

def get_reddit_data(api_client):
    # Initialize the Reddit client

    word_headmap = {} # Reddit comment dict of most used words in posts.
    reddit = api_client.get_reddit_api_client()
    subreddit = reddit.subreddit('stocks') # Dont use Stock it gets you data on soup and shit...
    top_posts = subreddit.hot(limit=2) # Set limit on how many posts are returned.

    # If we want to search reddit we can use the code below, i am not sure how that works in terms of requests. 
    #search_query = 'Rate My Portfolio'
    #Perform the search
    #search_results = subreddit.search(search_query, sort='new', limit=10)

    def get_comments(submission):
        submission.comments.replace_more(limit=None)
        comments = []
        for comment in submission.comments.list():
            comments.append({
                'author': str(comment.author),
                'body': comment.body,
                'score': comment.score,
                'created_utc': comment.created_utc
            })
        return comments
    data = []
    for post in top_posts:
        post_data2 = {
            'id': post.id,
            'title': post.title,
            'score': post.score,
            'url': post.url,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'author': str(post.author),
            'comments': get_comments(post)
        }
        data.append(post_data2)

    data = get_word_freq(data)
    json_data = json.dumps(data, indent=4)
    print(str(json_data))
    return json_data

def tokenize(text):
    # Sterilize the words in the comments.  
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def count_comment_words(comments):
    #using the Counter import we get a dict of number of words.
    all_words = []
    for comment in comments:
        all_words.extend(tokenize(comment['body']))
    return Counter(all_words)

def get_word_freq(data):
    results = {}
    for post in data:
        title = post['title']
        comments = post['comments']
        word_freq = count_comment_words(comments)

        filtered_sorted_word_freq = {word: freq for word, freq in word_freq.items() if freq >= 5} # remove words that occur 5 or less
        sorted_word_freq = dict(sorted(filtered_sorted_word_freq.items(), key=lambda item: item[1], reverse=True)) # rank highlest to lowest 
        results[title] = dict(sorted_word_freq)

    return results

def search_reddit_data(api_client, range, searchwords):
    """ This method takes in the api_client and a time range and returns reddit posts 
    api-client: api_client
    range: time range to search reddit over
    searchwords: strings to search over
    """
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    start_epoch = int(start_date.timestamp())
    end_epoch = int(end_date.timestamp())



    reddit = api_client.get_reddit_api_client()
    api = PushshiftAPI(reddit)


    
def get_news(news_key, beginning_date, ending_date):
    newsapi = NewsApiClient(news_key)
    end_date = datetime.now()
    start_date = end_date - relativedelta(months=1)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

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
        published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        published_date = published_at.date()
        if start_date <= published_at <= end_date:
            trending_stories[article['title']]=published_at.date()

    # Print the top headlines
    for article in top_headlines['articles']:
        published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        published_date = published_at.date()
        trending_stories[article['title']]=published_at.date()
    #print(trending_stories)
    return trending_stories

def plotstock(api_client):
    # Keeping this around for now just with the working consecutive closing price part of the code.
    dates = []
    closing_prices = []

    dates = list(data['Time Series (Daily)'].keys())[::-1]  # Reverse the order to plot from oldest to newest
    closing_prices = [float(data['Time Series (Daily)'][date]['4. close']) for date in dates]
    symbol = data['Meta Data']['2. Symbol']

    # This method needs to be moved elsewhere
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

def get_dummy_data(api_client): # return presaved stock json objs.
    ticker=api_client.get_ticker()
    if ticker == 'NVDA' or ticker == 'nvda':
        with open('../dummy_data/NVDA.json', 'r') as file:
            return json.load(file)
    elif ticker == 'AAPL' or ticker == 'aapl':
        with open('../dummy_data/AAPL.json', 'r') as file:
          return json.load(file)
    else:
        error_exit("Error: When using dummy flag specify wither NVDA or AAPL as the ticker.")

def get_consecutive_down_days(data):
    # Extract the time series data and convert it to a DataFrame
    time_series_data = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Convert the close prices to numeric
    df['4. close'] = pd.to_numeric(df['4. close'])

    # Initialize variables to store consecutive down day periods
    consecutive_down_days = 0
    start_date = None
    down_periods = []

    # Iterate through the DataFrame to identify down periods
    for i in range(1, len(df)):
        if df['4. close'].iloc[i] < df['4. close'].iloc[i-1]:
            if consecutive_down_days == 0:
                start_date = df.index[i-1]
            consecutive_down_days += 1
        else:
            if consecutive_down_days >= 5:
                end_date = df.index[i-1]
                down_periods.append((start_date, end_date))
            consecutive_down_days = 0

    # Check if the last period was a down period
    if consecutive_down_days >= 5:
        end_date = df.index[-1]
        down_periods.append((start_date, end_date))

    return down_periods
                
