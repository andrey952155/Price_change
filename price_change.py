import json

import requests
import websocket


class PriceChange:
    __url = f'wss://stream.binance.com:9443/stream?streams='
    flag = False

    @staticmethod
    def websocket_url():
        return PriceChange.__url[:-1]

    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        PriceChange.__url += f'{self.symbol}@kline_{self.timeframe}/'
        self.old_prices: list = self.get_old_prices()

    def get_old_prices(self):
        r = requests.get('https://api4.binance.com/api/v3/klines',
                         params={'symbol': self.symbol.upper(), 'interval': self.timeframe, 'limit': '61'})
        r = r.json()
        r = [float(item[4]) for item in r]
        return r

    def update_prices(self, current_price: float, is_candle_closed: bool):
        if is_candle_closed:
            self.old_prices.pop(0)
            self.old_prices.append(current_price)
            self.old_prices[:-1] = current_price

    def price_change(self):
        # процентное изменение считаем так ((V2-V1)/V1) × 100
        return ((self.old_prices[-1] - self.old_prices[0])/self.old_prices[0])*100


btcusdt = PriceChange('btcusdt', '1m')
ethusdt = PriceChange('ethusdt', '1m')


def on_message(ws, message):
    message = json.loads(message)
    message = message['data']['k']
    current_price = float(message['c'])
    is_candle_closed = message["x"]
    if message['s'] == 'BTCUSDT':
        btcusdt.update_prices(current_price, is_candle_closed)
    elif message['s'] == 'ETHUSDT':
        ethusdt.update_prices(current_price, is_candle_closed)
    # print(btcusdt.price_change() - ethusdt.price_change())
    if abs((btcusdt.price_change() - ethusdt.price_change())) > 1 and PriceChange.flag is False:
        print(f'Собственная цена ETH изменилась на{btcusdt.price_change() - ethusdt.price_change()}%')
        PriceChange.flag = True
    elif abs((btcusdt.price_change() - ethusdt.price_change())) < 1 and PriceChange.flag is True:
        PriceChange.flag = False


ws = websocket.WebSocketApp(PriceChange.websocket_url(), on_message=on_message)
ws.run_forever()








