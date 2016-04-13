# -*- coding: utf-8 -*-
from tkinter import *
from BtcSpotAPI import BtcSpot
from Datatable import draw
from FiexdInvestment import fiexdInvestment
import json
import time

class BtcClient(Frame):
	#初始化apikey，secretkey,url
	apikey = ''
	secretkey = ''
	okcoinRESTURL = 'www.okcoin.cn'

	#现货API
	okcoinSpot = BtcSpot(okcoinRESTURL,apikey,secretkey)

	money = 2000
	coin = 0

	def __init__(self, master=None):
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.startButton = Button(self, text='开始', width='10', command=self.onStart)
		self.startButton.grid(row=0, column=0)
		self.stopButton = Button(self, text='结束', width='10')
		self.stopButton.grid(row=0, column=1)
		self.oneKeyBuyButton = Button(self, text='一键下单', width='10')
		self.oneKeyBuyButton.grid(row=1, column=0)
		self.oneKeySaleButton = Button(self, text='一键平仓', width='10')
		self.oneKeySaleButton.grid(row=1, column=1)

	def klineData():
		arrkline = okcoinSpot.kline('btc_cny','1min','1','1417536000000')
		oneKline = arrkline[0]
		openPrice = oneKline[1]
		upPrice = oneKline[2]
		downPrice = oneKline[3]
		overPrice = oneKline[4]
		print('开：' + '%s'%openPrice + '	高：' + '%s'%upPrice + '	低：' + '%s'%downPrice + '	收：' + '%s'%overPrice)
		return oneKline

	def arrKlineData(self, size = '1'):
		return self.okcoinSpot.kline('btc_cny','15min',size,'1417536000000')

	def onStart(self):
		arrData = self.arrKlineData('2880')
		price0 = []
		labels = []
		data = []
		overPrice = 0

		index = 0
		for oneKline in arrData:
			overPrice = oneKline[4]
			tradingvolume = oneKline[5]
			timeStamp = oneKline[0]

			arrTime = time.localtime(timeStamp / 1000)
			styleTime = time.strftime("%d",arrTime)
			index = index + 1

			price0.append(overPrice)
			labels.append('%s'%index)
			data.append({'price':overPrice,'volume':tradingvolume})

		draw(price0,labels)
		btcData = fiexdInvestment(self.money, self.coin, data)
		self.money = btcData['money']
		self.coin = btcData['coin']
		print("总价值：" + '%.2f'%(self.money + self.coin * overPrice))

		self.totalPrice = Label(self,text="总价值：" + '%.2f'%(self.money + self.coin * overPrice))
		self.totalPrice.grid(row=2, column=0)

app = BtcClient()
# 设置窗口标题:
app.master.title('BTC')
app.master.geometry('200x100')
# 主消息循环:
app.mainloop()

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