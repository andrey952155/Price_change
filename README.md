# Price_change
Определяем собственное изменение цены ETHUSDT за последний час (исключив влияние изменения цены BTCUSDT)


При запуске программы из API Binance получаем список цен закрытий 60 последних минутных свечей для пар BTCUSDT и ETHUSDT. Теперь мы можем посчитать на сколько изменился курс за последний час и соответственно собственное движение ETHUSDT на момент загрузки программы.
Далее подключаемся к вебсокету Binance и в реальном времени получаем актуальные цены, пересчитываем собственное движение, при необходимости печатаем результат в консоль. По истечении очередной минуты обновляем список хранимый цен за последний час. 

