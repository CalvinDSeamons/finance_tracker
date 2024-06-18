# Main method to take in arguments set up API_Cleint Obj and Tkinter Gui Obj.
# This is the method that should be launched with python3 main.py

# Imports 
import argparse

# Imports from other classes within program
import get_stock_info
from tkintergui import launch_gui


def main(args):
    ticker, news, config, dummy, gui, webscraper = args
    # Main method creates the api_client objects and kicks off argparse actions.
    if gui: # If the user wants the gui, launch tkinter. Data will be set through there. 
       launch_gui()

    else:
        api_client = get_stock_info.APIClient(config, ticker, dummy, news, webscraper) # Create API Obj with argparser.
        #api_client.test()
        #api_client.get_ticker()
        #api_client.get_news_keywords()
        #get_stock_info.plotstock(api_client)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Command line inputs for stockapp") # Create argparse object.

    # Collecting possible arguments supplied via command line.
    parser.add_argument("--ticker", "-t", type=str, help="Stock Market Ticker, This value is required. Usage: --ticker=AAPL")
    parser.add_argument("--news",   "-n", nargs='*', type=str, help="Keywords to associate to online news. Usage: --news=Biden,apple,Gaza,Planecrash")
    parser.add_argument("--config", "-c", help="Yaml Configuration file containing the api keys. "
                                               "This will override default config. Usage: --config='path_to_your_config"
                                               , default='../configs/api-client2.yaml')
    parser.add_argument("--dummy",  "-d", action='store_true', help="If APIs request limit has been reached dummy will use saved static data. "
                                                                     "Usage: -d or --dummy")
    parser.add_argument("--gui", "-g", action='store_true', help="Launches a user GUI, flags such as ticker, and news will be overridden. "
                                                                  "Usage: -g ot --gui")
    parser.add_argument("--webscraper","-ws", nargs='*', type=str, help="Keywords to associte to online news, using webscraping instead of apis, slower but more data. "
                                                                        "Usage: --webscraper=Turtle, tree, plane" )

    
    args = parser.parse_args() # args is now a list of the possible arguments.
    args=([args.ticker, args.news, args.config, args.dummy, args.gui, args.webscraper])
    main(args) # Pass args to main method for execution. 