import argparse
import json
import matplotlib.pyplot as plt
import requests
import yaml

from newsapi import NewsApiClient
from datetime import datetime, timedelta

def get_stock_data(ticker, stock_key):
    print(stock_key)
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

def get_news(news_key):
    print(news_key)
    newsapi = NewsApiClient(news_key)

    # Define the time window
    start_date = datetime.now() - timedelta(days=7)  # 7 days ago
    end_date = datetime.now()  # Current date

    # Format the dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

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
        print(article['description'])
        print(article['url'])
        print() 


def plotstock(ticker, stock_key, dummy):

    if dummy:
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
        data = get_stock_data(ticker, stock_key)

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



    plt.figure(figsize=(16, 8))
    plt.plot(dates, closing_prices, marker='o', linestyle='-')

    plt.scatter([dates[i] for i in consecutive_lower_closes], 
            [closing_prices[i] for i in consecutive_lower_closes], 
            color='red', zorder=5, label='Consecutive Lower Closes')

    plt.title(symbol+' Closing Prices')
    plt.xlabel('Date',rotation=135)
    plt.ylabel('Closing Price ($)')
    plt.tight_layout()
    plt.show()
    

def main(args):
    ticker, news, config, dummy = args

    with open(config, "r") as file:
        # Load the YAML data
        data = yaml.safe_load(file)
    news_key = data["world_news_api_key"]
    stock_key = data["stock_data_api_key"]
    plotstock(ticker, stock_key, dummy)
    #get_news(news_key)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Command Line Inputs for stockapp")

    parser.add_argument("--ticker", "-t", type=str, help="Ticker symbol for stock", required=True)
    parser.add_argument("--news",   "-n", type=str, help="Fetch news for the specified ticker")
    parser.add_argument("--config", "-c", help="Yaml Configuration file containing the api keys", default='../configs/worldnews_stock__correlation.yaml')
    parser.add_argument("--dummy",  "-d", action='store_true', help="Using a static json for stock data, useful when api-limit is reached")

    args = parser.parse_args()

    if not args.ticker:
        parser.error("Please provide a stock trading ticker.")
    args=([args.ticker, args.news, args.config, args.dummy])
    main(args)