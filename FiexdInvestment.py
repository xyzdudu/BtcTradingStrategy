# -*- coding: utf-8 -*-
from BtcTransaction import buyBtc,saleBtc

PRE_VALUE = 200

#固定价值投资策略
def fiexdInvestment(money, coin, datas):
	value = 0	#价值
	preBuy = 0
	startPrice = 0	#第一次购买的价格
	standardNetWorth = 0	#标准净值
	standardValue = 0	#标准价值=价值/标准净值
	lastStandardValue = 0
	lastBuy = 0
	totalBuy = 0
	isStartBuy = True
	isUp = False
	isDown = False
	isVolumeUp = False	#放量上涨
	isVolumeDown = False	#放量下跌
	isNull = False

	lastTradingVolume = 0
	lastPrice = 0
	maxMoney = 0
	shockTime = 0

	for onedata in datas:
		price = onedata['price']
		tradingvolume = onedata['volume']

		# print("价格：" + '%s'%price + "	成交量：" + '%s'%tradingvolume)
		if startPrice == 0:
			startPrice = price
			lastTradingVolume = tradingvolume

		isVolumeDown = False
		if price > lastPrice:	#升
			isUp = True
			isDown = False
			if lastTradingVolume / tradingvolume >= 3:
				isVolumeUp = True
				isVolumeDown = False
				# print('放量上涨')
		elif price < lastPrice: #跌
			isUp = False
			isDown = True
			if lastTradingVolume / tradingvolume >= 1.2 or tradingvolume >= 8000:
				isVolumeUp = False
				isVolumeDown = True
				# print('放量下跌')
				shockTime = 0

				if coin == 0:
					isNull = True
					continue

		if isNull == True and coin == 0 and price - lastPrice <= 5 and price - lastPrice >= -5:
			shockTime = shockTime + 1
			if shockTime < 5:	#空仓时，没在震荡期不买入
				continue
		else:
			shockTime = 0

		standardNetWorth = 1 / startPrice * price
		value = value + PRE_VALUE
		standardValue = value / standardNetWorth
		preBuy = (standardValue - lastStandardValue) * standardNetWorth
		preCoin = preBuy / price
		lastStandardValue = standardValue
		lastPrice = price

		profit = 0
		btcData = {}
		if isStartBuy == False:
			profit = coin * price - totalBuy
			# print("盈利：" + '%.2f'%profit)
		#前面有大涨但现在跌了或不再放量了or放量下跌且不够钱
		if (isVolumeUp == True and (isDown == True or lastTradingVolume / tradingvolume < 3)) or (money - preBuy <= 0 and isVolumeDown == True):

			btcData = saleBtc(money, coin, price, coin)

			if isVolumeUp == True and (isDown == True or lastTradingVolume / tradingvolume < 2):
				isVolumeUp = False
				isVolumeDown = False
			totalBuy = 0
			startPrice = 0
			value = 0
			lastStandardValue = 0
			lastBuy = 0
			isStartBuy = True

			if btcData:
				money = btcData['money']
				coin = btcData['coin']

			#放量下跌且不够钱时，从新买回
			if money - preBuy <= 0 and isVolumeDown == True:
				isStartBuy = False

				btcData = buyBtc(money, coin, price, preCoin)
				if btcData:
					totalBuy = totalBuy + price * preCoin
					lastBuy = price * preCoin

		else:
			isStartBuy = False

			btcData = buyBtc(money, coin, price, preCoin)
			if btcData:
				totalBuy = totalBuy + price * preCoin
				lastBuy = price * preCoin

		if btcData:
			money = btcData['money']
			coin = btcData['coin']

		if money + coin * price > maxMoney:
			maxMoney = money + coin * price

	print('历史最高价值：' + '%.2f'%maxMoney)
	return {'money':money, 'coin':coin}