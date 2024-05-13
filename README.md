# StockSleuth: Unveiling Market Insights - A Fusion of Stock Analysis and Web Intelligence
***
### Introduction
This repository is a collection of scripts intended for categorizing world events, social media posts, and other potentially influential indicators to compare to stock trends. As of right now this software can only be used for past data as real-time api's are too expensive for an in-development app. Furthermore, stock queries cannot exceed 25 request per day, if this app proves usefull than upgrading to paid APIs will be necessary.


To use this software you must have: **newsapi, matplotlib, requests** and **argparse** installed in your python environment. Check the list imports if any other errors occur.

The the two API's used are alphavantage.co and newsapi. Both offer free developer keys at:<br />
    [NewsAPI](https://newsapi.org)<br />
    [AlphaVantage](https://www.alphavantage.co)<br />

Place your keys in the worldnews_stock_correlation.yaml in the configs directory. 


