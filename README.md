# StockSleuth: Unveiling Market Insights - A Fusion of Stock Analysis and Web Intelligence
***
### Introduction
This repository is a collection of scripts intended for analyzing world events, social media posts/trends, and other potentially influential indicators to compare against market trends. In essence this is web intelligence and how it can relate to the stock market and other finicial institutions. 


This software requires a lot of imports I recommend setting up a python virtual environment as follows: 
```bash
git clone $this_repository/
cd finance_tracker
python3 -m venv /path/to/finance_tracker/stocksleuth-virtual-env #stocksleuth-virtual-env can be named whatever you want.
source stocksleuth-virtal-env/bin/activate
deactivate #This will exit the python virtual env.
```
You'll now be inside the python virtual environment and can install the needed libraries without effecting your personal machine.

Below is a list of apis and accounts needed to use this software. Once obtained fill out configs/api-client.yaml<br />
- [NewsAPI](https://newsapi.org) Free API Key, requires throwaway email.
- [AlphaVantage](https://www.alphavantage.co) Free API Key, requires throwaway email. 
- [RedditAPI](https://www.reddit.com) Free API Key, create a reddit user, remember username and password.
    - [Reddit-App-Creation](https://www.reddit.com/prefs/apps) Log into reddit and create a reddit app named stocksleuth.
    - [Submit Request for API](https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id=14868593862164) Fill out this with the following:
        - Assistance with? -- API support an inqueries.
        - What Position? -- I am a Developer. 
        - Inquiry? -- I want to register to use the free tier of the Reddit API.
        - OAUTH Cleint ID? -- Give ID given during creation of Reddit App "stocksleuth" above.
        - You will be emailed Reddit Client-Secret, you now have all three pieces to use RedditAPI as defined in api-client.yaml

Run ```python3 get_stock_info.py -h ``` to get a list of avaible flags, use ```--gui``` or ```-g``` to launch the GUI if you dont like the command line.


