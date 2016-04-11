# -*- coding: utf-8 -*-
from BtcSpotAPI import BtcSpot
from Datatable import draw
import json
import time

#初始化apikey，secretkey,url
apikey = ''
secretkey = ''
okcoinRESTURL = 'www.okcoin.cn'

#2个上波浪，2个下波浪
MAX_UPWAVE = 2
MAX_DOWNWAVE = 2

PRE_VALUE = 500

#现货API
okcoinSpot = BtcSpot(okcoinRESTURL,apikey,secretkey)

def klineData():
	arrkline = okcoinSpot.kline('btc_cny','1min','1','1417536000000')
	oneKline = arrkline[0]
	openPrice = oneKline[1]
	upPrice = oneKline[2]
	downPrice = oneKline[3]
	overPrice = oneKline[4]
	print('开：' + '%s'%openPrice + '	高：' + '%s'%upPrice + '	低：' + '%s'%downPrice + '	收：' + '%s'%overPrice)
	return oneKline

def arrKlineData(size = '1'):
	return okcoinSpot.kline('btc_cny','15min',size,'1417536000000')

#波浪策略
def waveStrategy():
	money = 10000
	coin = 0

	upWave = 0
	downWave = 0
	lastUpPrice = 0
	lastDownPrice = 0
	lastOverPrice = 0

	oneKline = klineData()
	lastUpPrice = oneKline[2]
	lastDownPrice = oneKline[3]
	lastOverPrice = oneKline[4]

	while True:
		time.sleep(1 * 60)
		oneKline = klineData()
		upPrice = oneKline[2]
		downPrice = oneKline[3]
		overPrice = oneKline[4]
		if overPrice > lastOverPrice:#一个上波浪
			upWave = upWave + 1
			downWave = 0
			lastOverPrice = overPrice

		if overPrice < lastOverPrice:#一个下波浪
			downWave = downWave + 1
			upWave = 0
			lastOverPrice = overPrice

		if  money > 0 and downWave >= MAX_DOWNWAVE:
			print('买')
			coin = money / overPrice
			money = 0
			upWave = 0
			downWave = 0
		elif coin > 0 and upWave >= MAX_UPWAVE:
			print('卖')
			money = coin * overPrice
			coin = 0
			upWave = 0
			downWave = 0
		print('钱：' + '%s'%money + "	币：" + '%s'%coin)

#定投策略
def fiexdInvestment():
	money = 2000
	coin = 0
	value = 0	#价值
	preBuy = 0
	startPrice = 0	#第一次购买的价格
	standardNetWorth = 0	#标准净值
	standardValue = 0	#标准价值=价值/标准净值
	lastStandardValue = 0
	lastBuy = 0
	totalBuy = 0
	isStartBuy = True

	while True:
		print(time.strftime("%Y-%m-%d %H:%M"))

		oneKline = klineData()
		upPrice = oneKline[2]
		downPrice = oneKline[3]
		overPrice = oneKline[4]

		if startPrice == 0:
			startPrice = overPrice

		standardNetWorth = 1 / startPrice * overPrice
		value = value + PRE_VALUE
		standardValue = value / standardNetWorth
		preBuy = (standardValue - lastStandardValue) * standardNetWorth
		preCoin = preBuy / overPrice
		lastStandardValue = standardValue

		profit = 0
		if isStartBuy == False:
			profit = coin * overPrice - totalBuy
			print("盈利：" + '%.2f'%profit)
		if profit >= 0.5 or profit <= -1:
			money = money + coin * overPrice
			coin = 0
			totalBuy = 0
			startPrice = 0
			value = 0
			lastStandardValue = 0
			lastBuy = 0
			isStartBuy = True
			print("卖	RMB：" + '%.2f'%money + "	btc：" + '%.4f'%coin)
		elif money - preBuy > 0:
			money = money - preBuy
			coin = coin + preCoin
			totalBuy = totalBuy + preBuy
			lastBuy = preBuy
			isStartBuy = False
			print("买	RMB：" + '%.2f'%money + "	btc：" + '%.4f'%coin + "	购买：" + '%.2f'%preBuy)

		print("总价值：" + '%.2f'%(money + coin * overPrice))

		time.sleep(1 * 60)

def fiexdInvestment2(datas):
	money = 2000
	coin = 0
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
	overPrice = 0

	lastTradingVolume = 0
	lastPrice = 0
	maxMoney = 0
	shockTime = 0

	for onedata in datas:
		price = onedata['price']
		overPrice = price
		tradingvolume = onedata['volume']

		# print("价格：" + '%s'%price + "	成交量：" + '%s'%tradingvolume)
		if startPrice == 0:
			startPrice = price
			lastTradingVolume = tradingvolume

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
		if isStartBuy == False:
			profit = coin * price - totalBuy
			# print("盈利：" + '%.2f'%profit)
		if profit > 0 or (money - preBuy <= 0 and profit > 0) or (isVolumeDown == True) or (isVolumeUp == True and (isDown == True or lastTradingVolume / tradingvolume < 3)):
			if isVolumeDown == True or (isVolumeUp == True and (isDown == True or lastTradingVolume / tradingvolume < 2)):
				isVolumeUp = False
				isVolumeDown = False
			money = money + coin * price
			coin = 0
			totalBuy = 0
			startPrice = 0
			value = 0
			lastStandardValue = 0
			lastBuy = 0
			isStartBuy = True
			# print("卖	RMB：" + '%.2f'%money + "	btc：" + '%.4f'%coin + "	价格：" + '%s'%price)
		elif money - preBuy > 0:
			money = money - preBuy
			coin = coin + preCoin
			totalBuy = totalBuy + preBuy
			lastBuy = preBuy
			isStartBuy = False
			isNull = True
			# print("买	RMB：" + '%.2f'%money + "	btc：" + '%.4f'%coin + "	购买：" + '%.2f'%preBuy + "	价格：" + '%s'%price)

		if money + coin * price > maxMoney:
			maxMoney = money + coin * price

	print("总价值：" + '%.2f'%(money + coin * overPrice) + "	历史最高价值：" + '%.2f'%maxMoney)

if __name__ == '__main__':
	#fiexdInvestment()
	# draw()
	arrData = arrKlineData('2880')
	price0 = []
	labels = []
	data = []

	for oneKline in arrData:
		overPrice = oneKline[4]
		tradingvolume = oneKline[5]
		timeStamp = oneKline[0]
		arrTime = time.localtime(timeStamp / 1000)
		styleTime = time.strftime("%H:%M",arrTime)
		price0.append(overPrice)
		labels.append('%s'%styleTime)
		data.append({'price':overPrice,'volume':tradingvolume})

	# draw(price0,labels)

	fiexdInvestment2(data)
		
# print(u'现货行情')
# print(okcoinSpot.ticker('btc_cny'))

# print (u' 现货深度 ')
# print (okcoinSpot.depth('btc_cny'))

#print (u' 现货历史交易信息 ')
#print (okcoinSpot.trades())

# print (u' 用户现货账户信息 ')
# print (okcoinSpot.userinfo())

#print (u' 现货下单 ')
#print (okcoinSpot.trade('ltc_usd','buy','0.1','0.2'))

#print (u' 现货批量下单 ')
#print (okcoinSpot.batchTrade('ltc_usd','buy','[{price:0.1,amount:0.2},{price:0.1,amount:0.2}]'))

#print (u' 现货取消订单 ')
#print (okcoinSpot.cancelOrder('ltc_usd','18243073'))

#print (u' 现货订单信息查询 ')
#print (okcoinSpot.orderinfo('ltc_usd','18243644'))

#print (u' 现货批量订单信息查询 ')
#print (okcoinSpot.ordersinfo('ltc_usd','18243800,18243801,18243644','0'))

#print (u' 现货历史订单信息查询 ')
#print (okcoinSpot.orderHistory('ltc_usd','0','1','2'))

#print (u' 期货行情信息')
#print (okcoinFuture.future_ticker('ltc_usd','this_week'))

#print (u' 期货市场深度信息')
#print (okcoinFuture.future_depth('btc_usd','this_week','6'))

#print (u'期货交易记录信息') 
#print (okcoinFuture.future_trades('ltc_usd','this_week'))

#print (u'期货指数信息')
#print (okcoinFuture.future_index('ltc_usd'))

#print (u'美元人民币汇率')
#print (okcoinFuture.exchange_rate())

#print (u'获取预估交割价') 
#print (okcoinFuture.future_estimated_price('ltc_usd'))

#print (u'获取全仓账户信息')
#print (okcoinFuture.future_userinfo())

#print (u'获取全仓持仓信息')
#print (okcoinFuture.future_position('ltc_usd','this_week'))

#print (u'期货下单')
#print (okcoinFuture.future_trade('ltc_usd','this_week','0.1','1','1','0','20'))

#print (u'期货批量下单')
#print (okcoinFuture.future_batchTrade('ltc_usd','this_week','[{price:0.1,amount:1,type:1,match_price:0},{price:0.1,amount:3,type:1,match_price:0}]','20'))

#print (u'期货取消订单')
#print (okcoinFuture.future_cancel('ltc_usd','this_week','47231499'))

#print (u'期货获取订单信息')
#print (okcoinFuture.future_orderinfo('ltc_usd','this_week','47231812','0','1','2'))

#print (u'期货逐仓账户信息')
#print (okcoinFuture.future_userinfo_4fix())

#print (u'期货逐仓持仓信息')
#print (okcoinFuture.future_position_4fix('ltc_usd','this_week',1))

# userData = okcoinSpot.userinfo()
# print(userData)

# userData = json.loads(userData)
# if userData['result']:
# 	info = userData['info']
# 	funds = info['funds']
# 	asset = funds['asset']
# 	free = funds['free']
# 	freezed = funds['freezed']
# 	print('净资产：'+'%s'%asset['net']+'	总资产：'+'%s'%asset['total'])
# 	print('btc：'+'%s'%free['btc']+'	RMB：'+'%s'%free['cny'])