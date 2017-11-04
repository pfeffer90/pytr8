# HOW TO

```
python src/pytrade.py
```

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
  - When active, our Python Script continiously performs the following steps:
    - Get Price data for a specified Asset Pair (*BTCUSD*) in regular (10 seconds?) intervals
    - Computes trading signals (can be adjusted by the user, for illustrative purposes we implement a momentum strategy: If the    price at time *t* is larger than the price at *t+1*, the signal is 1, otherwise it is -1/ no change: 0)
    - If the trading signal is 1 or -1 and our simple risk management tool allows for further trades, a market order is placed (either buy or sell)
    - The script continiously creates a log-file which contains the signal values, the corresponding actions, and checks if the trades are settled.
  - Risk management: To avoid extreme positions we force the algorithm to check certain risk measures before submitting a trade order. To keep the setup simple, for now we simply restrict ourselves to sending at max. one buy signal. Afterwards, only sell orders are allowed which keeps our exposure to Bitcoin small. 
* Regelmäßiges abrufen eines Preises von einer (existierenden) API
  - wie oft?
    - falls täglich, stündlich, würde sich eine Lösung außerhalb von Python anbieten zum Beispiel *cron tab*
    - falls kontinuierlich, laufendes Programm
* Speichern des Preises
    - wie oft und wie lange?

* Berechnen von irgendeinem kruden Wert als Signal
    - komplex? Nö
    - is speed important? Nö
* If Wert > irgendwas Kaufsignal an API.
    - was für Berechtigungen brauchen wir da? Der Zugang zu einem Wallet benötigt einen access token, ich habe bereits angefragt. Das Abrufen der Preise etc. geht allerdings ohne jegliche Berechtigung (meines Wissens ist auch kein Limit eingebaut).
