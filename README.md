**Warning: Connecting the trading enginge with your wallet may cause real losses - we do not take any responsibility for any errors in the code or unfortunate market movements which may work against you!**

# A simple Python framework for trading algorithms running on [Lykke](www.lykke.com) 

This repository hosts our submission for the [Lykke stream](https://streams.lykke.com/Project/ProjectDetails/python-simple-trading-algorithm-development) which aims at making the [Lykke API](https://hft-service-dev.lykkex.net/swagger/ui/index.html#/) more user (and robot) friendly. Feel free to fork and extend this repository, share your thoughts, and spread the idea of the first blockchain based Exchange. Functionalities of this framework include:
- Ongoing price flow maintenance for all available asset pairs 
- Automatic processing of price information to generate trading signals
- Trading signals are processed by risk management engine before sending out orders
- Automatic submission of Market (and Limit) orders 
- Supervision of order status as a risk management functionality
- The framework ensures that all functionalities are saved in a log-file, providing information for debugging to improve the code in testing environments or to ensure compliance. 

Everything is set up as a minimal example and can easily be extended. 

# Prerequisites

## For installation

First, you need the [lykkex](https://github.com/pfeffer90/lykkex) module, which is a simple wrapper for the Lykkex API for easy use with python. To install it
```bash
git clone git@github.com:pfeffer90/lykkex.git
cd lykkex
pip install .
```

With this dependency fulfilled, use the provided setup.py to install pytr8
  
```bash
pip install .
```

## For using the API

You need an [API access token to communicate with the Lykkex API and access your wallet](https://www.lykke.com/lykke_api). 


# HOW TO

Start the trade bot by
```
pytr8 -f <path_to_config_file>
```
and stop it by Ctrl-C. To try out the trade bot, use the provided configuration file [demo_config.json](./demo_config.json). For more options e.g. logging settings, check out 
```
pytr8 -h 
``` 

To get a summary of the trading actions, check the content of the database
```
sqlite3 <path_to_db> 'select * from trading_actions'
```

The trading algorithm fetches prices quoted at Lykke and stores them in a database.
To load price series:
    - import `DBService` with the path to the database with which the trade bot was running
    - call `get_price_data` and you will get a [Pandas](https://pandas.pydata.org/) data frame similar to **R** dataframe, which gives you all the data

# Detailed specification description

We create a trading algorithm in Python based on [the Lykke exchange](https://www.lykke.com/). The framework allows users to fetch current prices, to submit market and limit orders, and to track execution of the trades in a simple fashion. 

Platform:
  - We use the [HighFrequencyTrading API](https://hft-service-dev.lykkex.net/swagger/ui/index.html) provided by Lykke to interact with the exchange.
  - Functionalities of the API include:
    - Get available Asset Pairs 
    - Get the current state of the order book for specified asset pairs
    - Check the balance of a specified wallet
    - Submit market/ limit orders
    - Cancel existing orders
  - When active, our Python Script continuously performs the following steps:
    - Get Price data for a specified Asset Pair (*AUDUSD*) in regular intervals
    - Computes trading signals (can be adjusted by the user, for illustrative purposes we implement a version of a momentum strategy: If the    price at time *t* is larger than the mean price during the last *t-h* time periods, the signal is 1, otherwise it is -1/ no change: 0)
    - If the trading signal is 1 or -1 and our simple risk management tool allows for further trades, a market order is placed (either buy or sell)
    - The script continuously creates a log-file which contains the signal values, the corresponding actions, and checks if the trades are settled.
  - Risk management: To avoid extreme positions we force the algorithm to check certain risk measures before submitting a trade order. To keep the setup simple, for now we simply restrict ourselves to sending at max. one buy signal. Afterwards, only sell orders are allowed which keeps our exposure to Bitcoin small. 

# Some details (FAQ)

## Usage
* Which prior configurations are necessary to run the trading bot?
  * Before running the algorithm, configurations from the outside include:
    - asset pair (default = *AUDUSD*)
    - database file path
    - trading interval (default = *0.2 secs*)
    - time periods *h* to take the mean (default = *300* [1 minute])
* What happens if the script is interrupted and started again?
     - Errors are associated with the potential to loosing money. Therefore, any error should immediately lead to a full stop of   the script. 
    - Reasons to stop the script:
        1. API is not responding
        2. Prices are unreasonable (to be specified: for now we should send a signal if the price variation in our database is high, say, ratio of highest to lowest price during the last 60 observations (=10 minutes) is larger than 1.5)
    - Reasons to stop sending trading signals:
        1. Price history is not long enough (say, 2 minutes as default)
        1. Trades are awaiting verification

## Trading signals

* What is the input to a trade signal calculation?
   - The signal can be based on the history of past prices. 
* How does the default trading strategy look like?
   - Currently we run a strategy related to momentum. During the trading process, past prices are used to compute moving averages. If the current prices exceeds (falls below) a fixed threshold, a buy (sell) signal is triggered. 
* What about risk management?
   - Before the algo starts computing trade signals, the risk management tool has to confirm that trades are allowed. The tool checks a number of things (and can easily be extended): 1. Current balance 2. Latency of the system

## Database

* Which kind of data is stored?
   - A database is created which allows to extract the retrieved prices (this may be useful for backtesting of future stragies)
   - The trade log contains all necessary information to ensure the compliance of the algorithm. Time stamps, received trading signals, trading verifications, etc. are stored
