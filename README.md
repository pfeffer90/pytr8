**Warning: Connecting the trading enginge with your wallet may cause real losses - we do not take any responsibility for any errors in the code or unfortunate market movements which may work against you!**

# A simple Python framework for trading algorithms running on [Lykke](www.lykke.com) 

This repository hosts our submission for the [Lykke stream](https://streams.lykke.com/Project/ProjectDetails/python-simple-trading-algorithm-development) which aims at making the [Lykke API](https://hft-service-dev.lykkex.net/swagger/ui/index.html#/) more user (and robot) friendly. Feel free to fork and extend this repository, share your thoughts, and spread the idea of the first blockchain based Exchange. Features of this framework include:
- Ongoing price flow maintenance for all available asset pairs 
- Automatic processing of price information to generate trading signals
- Trading signals are processed by risk management engine before sending out orders
- Automatic submission of Market (and Limit) orders 
- Supervision of order status as a risk management functionality
- Persistence of trading orders in a lightweight database
- The framework ensures that all trading steps are saved in a log-file, providing information for debugging to improve the code in testing environments or to ensure compliance. 

Everything is set up as a minimal example and can easily be extended. 

# Prerequisites

## For installation

The required packages are specified in the setup.py. One which might be interesting is the [lykkex](https://github.com/pfeffer90/lykkex) module, which is a simple wrapper for the Lykkex API for easy use with python and which could be helpful for other projects. To install pytr8
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

To get a summary of the market orders, check the content of the database
```
sqlite3 <path_to_db> 'select * from market_orders'
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

# A minimal tutorial for pytr8 

We created [pytr8](https://github.com/pfeffer90/pytr8) to provide easy access to the blockchain-based Lykke exchange via Python. Setting up your own trading algo can now be done in just a few steps, whereas the framework is flexible enough to handle many different needs. 

*pytr8* provides you with 4 core functionalities:
- Getting data 
- Generating trading signals
- Risk management 
- Handling and processing of orders. 

## Getting data

*pytr8* approaches the Lykke API using [the simple lykkex wrapper](https://github.com/pfeffer90/lykkex). 
It enables to fetch latest data from the Lykke universe

Within our tradebot, we provide a database solution to track latest price developments:
`inform()` gets prices and volumes for a given asset pair on a regular basis and stores them in a easy to access pandas dataframe. Of course you can always extend the set of information which should be gathered by your trading bot.

Example: The fetched prices (BTCUSD) are not really provided on a real time basis by the Lykke API by now (this is going to change soon). However, the basic concept on how the set of information passed to the trade bot look should be clear...

                     timestamp  buy_price  sell_price
    0   2017-12-01 16:25:56.979242     9000.0    10524.97
    1   2017-12-01 16:25:59.168361     9000.0    10524.97
    2   2017-12-01 16:26:01.125344     9000.0    10525.00
    3   2017-12-01 16:26:02.799933     9000.0    10525.00
    4   2017-12-01 16:26:04.501000     9000.0    10525.00
    5   2017-12-01 16:26:06.252238     9000.0    10525.00
    6   2017-12-01 16:26:08.322539     9000.0    10525.00
    7   2017-12-01 16:26:10.248343     9000.0    10525.00
    8   2017-12-01 16:26:13.262828     9000.0    10521.76
    9   2017-12-01 16:26:14.931131     9000.0    10521.76
    10  2017-12-01 16:26:17.345537     9000.0    10521.76
    11  2017-12-01 16:26:19.024431     9000.0    10521.76
    12  2017-12-01 16:26:20.921102     9000.0    10511.80
    13  2017-12-01 16:26:22.604932     9000.0    10511.80
    14  2017-12-01 16:26:24.300936     9000.0    10511.80
    15  2017-12-01 16:26:26.180524     9000.0    10511.80
    16  2017-12-01 16:26:28.154511     9000.0    10511.80



## Making decisions
The core of the trade bot can be found within `calculate_trading_signal`:
Here, the information is used and processed to a signal, either `BUY` or `SELL`. `pytr8` currently comes with two, honestly speaking rather naive, trading algorithms:
- Random strategy: Created for testing purposes and fires out random buy and sell orders.
- Momentum strategy: Gives an example how to use past prices to create a trading signal: We compute the midquote time series given the bid and aks prices provided by our database service and send a buy signal to capture upswing in the markets. The equivalent holds for downswings: If our data detects a negative price movement averaged over the last couple of minutes, it returns a sell order.

Clearly, these strategies can be extended in many directions. However, if you have a look on the code underlying the momentum strategy it should be easy to adapt the trading signals to your very own needs.

## Let the pessimists speak
Although your trading signals may strongly indicate that you surely should buy, we enforce the trading bot to go through a simple risk management tool before the order is send out to the market. `evaluate()` currently checks if there are still orders (limit orders in particular) pending and awaiting verification. Further, the current balance is checked to ensure you have the funds to trade. The usual disclaimer appears here as well: One look in the code should make it very easy to expand the set of risk measures: The database service (see below) even provides you with the past history of actions, so you can also prevent trading if you already build up large positions in one direction.

Example where trading is allowed: Current wealth is sufficient to trade *and* no orders are pending:

    2017-12-01 16:16:25 INFO: Current wealth AUD: 781.2
    2017-12-01 16:16:25 INFO: Current wealth BTC: 0.91412796
    2017-12-01 16:16:25 INFO: Current wealth EUR: 731.15
    2017-12-01 16:16:25 INFO: Current wealth USD: 43.89
    2017-12-01 16:17:35 INFO: Get pending orders.
    2017-12-01 16:17:35 INFO: No pending orders
    2017-12-01 16:17:35 INFO: Trading stop: 0

## Send the Genie out of the bottle
    
After passing the risk management, our tradebot directly interacts with Lykke and send orders to the market - `act()` wraps the action and is up and ready to fire out market orders. You want limit orders instead? No problem: Just replace ´lykkex_service.send_market_order` with `lykkex_service.send_limit_order` and provide a limit price which fits your needs.

Example log file: Our algo sends out an order to sell a (predefined) amount of USD against BTC:

    2017-12-01 16:20:01 INFO: Trading signal: -1
    2017-12-01 16:20:01 INFO: Send selling signal
    2017-12-01 16:20:01 INFO: Send market order - USD
    2017-12-01 16:20:03 INFO: Trade successful at price 10491.66



## What did just happen?

Let it either be for back-testing, to swagger and to promote your trading skills, or simply to ensure compliance rules: Whatever you do, `pytr8` keeps care of creating log reports and tracks every single action of the trading bot. 


# Some details (FAQ)
* Which prior configurations are necessary to run the trading bot?
  * Before running the algorithm, configurations from the outside include:
    - asset pair (default = *AUDUSD*)
    - database file path
    - trading interval (default = *0.2 secs*)
    - time periods *h* to take the mean (default = *300* [1 minute])
* What is the input to a trade signal calculation?
   - The signal can be based on the history of past prices. 
* How does the default trading strategy look like?
   - Currently we run a strategy related to momentum. During the trading process, past prices are used to compute moving averages. If the current prices exceeds (falls below) a fixed threshold, a buy (sell) signal is triggered. 
* What about risk management?
   - Before the algo starts computing trade signals, the risk management tool has to confirm that trades are allowed. The tool checks a number of things (and can easily be extended): 1. Current balance 2. Latency of the system
* Which kind of data is stored?
   - A database is created which allows to extract the retrieved prices (this may be useful for backtesting of future stragies)
   - The trade log contains all necessary information to ensure the compliance of the algorithm. Time stamps, received trading signals, trading verifications, etc. are stored
