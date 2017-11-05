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
    - Computes trading signals (can be adjusted by the user, for illustrative purposes we implement a momentum strategy: If the    price at time *t* is larger than the price at *t+1*, the signal is 1, otherwise it is -1/ no change: 0)
    - If the trading signal is 1 or -1 and our simple risk management tool allows for further trades, a market order is placed (either buy or sell)
    - The script continuously creates a log-file which contains the signal values, the corresponding actions, and checks if the trades are settled.
  - Risk management: To avoid extreme positions we force the algorithm to check certain risk measures before submitting a trade order. To keep the setup simple, for now we simply restrict ourselves to sending at max. one buy signal. Afterwards, only sell orders are allowed which keeps our exposure to Bitcoin small. 


# QUESTIONS

## Usage
* what would you like to configure from the outside? e.g.
  - trading interval
  - asset pair
  - database file path
* what do we do if the script is interrupted and started again?
* how many instances of the script can run?

## Calculating the trade signal

* what is the input to a trade signal calculation?
   - only price list?
   - does the trader need a guarantee like constant time interval between price retrieval?
* currently, we compare the whole price history mean with the current price. this is not the momentum strategy, which was suggested in the plan. should this be changed?

## Database

* there seems to be two purposes of a database? on the one hand persisting the retrieved asset prices and on the other hand persisting the calculated trading signals and actions

### Price database

* how much price history does the trader use for the calculation of the trading signal?
* do we need further fields besides time stamp and price?

### Trading database
* which form does an entry have?
  - time_stamp, price, trading_signal, action, is_settled



## Wallet access token
* ?