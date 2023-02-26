import json
import pandas as pd
import datetime
import requests
import os
import matplotlib.pyplot as plt

def getStock(): 
    # get stock from user
    stock = input("Enter Stock: ")
    
    apikey="kUYPwODjJW1oSAgvnN8fU3wq8Paj6FPj1HRfqfPU"
    
    quote_url = "https://yfapi.net/v6/finance/quote"
    financialdata_url = f"https://yfapi.net/v11/finance/quoteSummary/{stock}?lang=en&region=US&modules=financialData"
    stockpricehistory_url = f"https://yfapi.net/v8/finance/chart/{stock}?comparisons=MSFT%2C%5EVIX&range=1mo&region=US&interval=1d&lang=en&events=div%2Csplit"
    
    querystring = {"symbols":stock}

    headers = {
        'x-api-key': apikey
        }
    
    
    response = requests.request("GET", quote_url, headers=headers, params=querystring)
    response2 = requests.request("GET", financialdata_url, headers=headers, params=querystring)
    response3 = requests.request("GET", stockpricehistory_url, headers=headers, params=querystring)
    # print(response.text)
    # print(response2.text)
    # print(response3.text)
    
    # Handling Errors accounted for below: 
    # if stock does not exist
    # if information cannot be retrieved from API
    # a combination of the two
    if response.status_code == 404 or response2.status_code == 404 or response3.status_code == 404:
        raise ValueError(f"{stock} is not a valid stock symbol")
    elif response.status_code != 200 or response2.status_code != 200 or response3.status_code != 200:
        raise Exception("Failed to retrieve stock information")
    else:
        stock_json = response.json()
        stock_json2 = response2.json()
        stock_json3 = response3.json()

    # If you want to print each piece of information per line
    
    # Information retrieved from stock_json
    # print("Name Ticker: " + stock_json['quoteResponse']['result'][0]["symbol"])
    # print("Full Name of Company: " + stock_json['quoteResponse']['result'][0]["displayName"] + ":")
    # print("Current Price: " + str(stock_json['quoteResponse']['result'][0]["regularMarketPrice"]))

    # Information retrieved from stock_json2
    # print("Target Mean Price: " + str(stock_json2['quoteSummary']['result'][0]['financialData']["targetMeanPrice"]['fmt']))
    # print("Cash on Hand: " + str(stock_json2['quoteSummary']['result'][0]['financialData']["freeCashflow"]['fmt']))
    # print("Profit Margins: " + str(stock_json2['quoteSummary']['result'][0]['financialData']["profitMargins"]['fmt']))

    # Store information in a dict
    stock_dict = {}
    timestamp = stock_json['quoteResponse']['result'][0]["regularMarketTime"]
    stock_dict["Date"] = [datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')]
    stock_dict["Name Ticker"] = stock_json['quoteResponse']['result'][0]["symbol"]
    stock_dict["Full Name of the Company"] = stock_json['quoteResponse']['result'][0]["displayName"]
    stock_dict["Current Price"] = "$" + str(stock_json['quoteResponse']['result'][0]["regularMarketPrice"])
    stock_dict["Target Mean Price"] = "$" + str(stock_json2['quoteSummary']['result'][0]['financialData']["targetMeanPrice"]['fmt'])
    stock_dict["Cash on Hand"] = "$" + str(stock_json2['quoteSummary']['result'][0]['financialData']["freeCashflow"]['fmt'])
    stock_dict["Profit Margins"] = str(stock_json2['quoteSummary']['result'][0]['financialData']["profitMargins"]['fmt'])

    # Convert dict to a dataframe
    # Opted to print as a dataframe to save more space rather than printing each piece of information
    df = pd.DataFrame(stock_dict, index=[0])
    
    print(f"Here is information about: {stock}")
    
    # For better visibility
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    print(df)
    
    # Save in home directory
    home_dir = os.path.expanduser("~")
    file_path = os.path.join(home_dir, 'stock_data.json')
    
    with open(os.path.join(home_dir,'stock_data.json'), 'w') as f:
        json.dump(stock_dict, f)
        
    print(f"stock_data.json was saved at: {file_path}")
    
    print(f"BONUS: Historical Highest Value of {stock} over the past 5 days")
    
    # Get historical stock prices
    timestamps = stock_json3["chart"]["result"][0]["timestamp"]
    prices = stock_json3["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    dates = [datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y') for timestamp in timestamps]
    
    # Find highest stock price over the past 5 days
    past_5_days_prices = prices[-5:]
    highest_price = max(past_5_days_prices)
    
    # Plot the highest stock price over the past 5 days
    plt.plot(dates[-5:], past_5_days_prices)
    plt.title("Highest Stock Price for {0} over the past 5 days".format(stock))
    plt.xlabel("Date")
    plt.ylabel("Highest Stock Price ($)")
    plt.annotate(f"Highest price: ${highest_price:.2f}", xy=(dates[-1], highest_price), xytext=(dates[-1], highest_price*1.01), fontsize=10, color="red", ha="center")
    plt.show()
    
getStock()