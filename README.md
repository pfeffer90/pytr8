# HOW TO

Start the program by
```
python src/pytrade.py
```
and stop it by Ctrl-C.

# PLAN

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
    - Get Price data for a specified Asset Pair (*BTCUSD*) in regular (10 seconds?) intervals
    - **The Lykke API currently does not support fetching BTCUSD data in real time. Instead, we use the pair AUDUSD to test our framework.**
    - Computes trading signals (can be adjusted by the user, for illustrative purposes we implement a version of a momentum strategy: If the    price at time *t* is larger than the mean price during the last *t-h* time periods, the signal is 1, otherwise it is -1/ no change: 0)
    - If the trading signal is 1 or -1 and our simple risk management tool allows for further trades, a market order is placed (either buy or sell)
    - The script continuously creates a log-file which contains the signal values, the corresponding actions, and checks if the trades are settled.
  - Risk management: To avoid extreme positions we force the algorithm to check certain risk measures before submitting a trade order. To keep the setup simple, for now we simply restrict ourselves to sending at max. one buy signal. Afterwards, only sell orders are allowed which keeps our exposure to Bitcoin small. 


# QUESTIONS

## Usage
* Configurations from the outside include:
  - asset pair (default = *BTCUSD*)
  - database file path
  - trading interval (default = *10 secs*)
  - time periods *h* to take the mean (default = *6* [1 minute])
* what do we do if the script is interrupted and started again?
    - Errors are associated with the potential to loosing money. Therefore, any error should immediately lead to a full stop of the script. 
    - Reasons to stop the script:
        1. API is not responding
        2. Prices are unreasonable (to be specified: for now we should send a signal if the price variation in our database is high, say, ratio of highest to lowest price during the last 60 observations (=10 minutes) is larger than 1.5)
    - Reasons to stop sending trading signals:
        1. Price history is not long enough (say, 2 minutes as default)
        1. Trades are awaiting verification
* how many instances of the script can run?
    - The script is connected to one wallet id. To ensure global risk management is working properly, trading signals should be restricted to be send from one instance for each currency pair.

## Calculating the trade signal

* what is the input to a trade signal calculation?
   - For the sake of brevity we use only price list
   - does the trader need a guarantee like constant time interval between price retrieval? (what does this mean?) 
* currently, we compare the whole price history mean with the current price. this is not the momentum strategy, which was suggested in the plan. should this be changed? **Already Changed**

## Database

* there seems to be two purposes of a database? on the one hand persisting the retrieved asset prices and on the other hand persisting the calculated trading signals and actions

### Price database

* how much price history does the trader use for the calculation of the trading signal?
* do we need further fields besides time stamp and price?
* Required fields:
    - Time stamp
    - Ask price (Best price on the sell level (= lowest price))
    - Bid price (Best price on the buy level (=highest pice))

### Trading database
* which form does an entry have?
  - time_stamp, price, trading_signal, action, is_settled



## Wallet access token
* ?
