import argparse
import json
import matplotlib.pyplot as plt
import requests
import yaml

def get_stock_data(ticker, stock_key):
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


def plotstock(ticker, stock_key):
    data = get_stock_data(ticker, stock_key)
    #data = json.loads(data)
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



    plt.figure(figsize=(10, 6))
    plt.plot(dates, closing_prices, marker='o', linestyle='-')

    plt.scatter([dates[i] for i in consecutive_lower_closes], 
            [closing_prices[i] for i in consecutive_lower_closes], 
            color='red', zorder=5, label='Consecutive Lower Closes')

    plt.title(symbol+' Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Closing Price ($)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()
    

def main(ticker, news, config):
    with open(config, "r") as file:
        # Load the YAML data
        data = yaml.safe_load(file)
    news_key = data["world_news_api_key"]
    stock_key = data["stock_data_api_key"]
    plotstock(ticker, stock_key)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Command Line Inputs for stockapp")

    parser.add_argument("--ticker", "-t", type=str, help="Ticker symbol for stock", required=True)
    parser.add_argument("--news",   "-n", type=str, help="Fetch news for the specified ticker")
    parser.add_argument("--config", "-c", help="Yaml Configuration file containing the api keys", default='../configs/worldnews_stock__correlation.yaml')

    args = parser.parse_args()

    if not args.ticker:
        parser.error("Please provide a stock trading ticker.")
    
    main(args.ticker, args.news, args.config)