import matplotlib.pyplot as plt
import json
import requests

def get_stock_data(symbol):



    api_key=''
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def get_news_data():
    #bleh bleh news idk
    news_api_key = ''
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

if __name__ == "__main__":
    #Creating ARG Parser
    #parser = argparse.ArgumentParser(description="finacial inqueires")

    symbol = 'NVDA'  # Example stock symbol (Apple Inc.)
    data = get_stock_data(symbol)
    #data = json.loads(data)
    dates = []
    closing_prices = []

    for date, values in data["Time Series (Daily)"].items():
        dates.append(date)
        closing_prices.append(float(values["4. close"]))

# Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(dates, closing_prices, marker='o', linestyle='-')
    plt.title('Closing Prices of NVDA')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.gca().invert_xaxis()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    
