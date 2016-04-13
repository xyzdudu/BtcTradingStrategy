# -*- coding: utf-8 -*-
#BTC交易

#买
def buyBtc(money, coin, price, buyCoin):
	buyMoney = buyCoin * price
	if money - buyMoney > 0:
		money = money - buyMoney
		coin = coin + buyCoin
		# print("买	RMB：" + '%.2f'%money + "	btc：" + '%.4f'%coin + "	购买：" + '%.2f'%(price * buyCoin) + "	价格：" + '%s'%price)
		return {'money':money, 'coin':coin}
	return None


#卖
def saleBtc(money, coin, price, saleCoin):
	money = money + saleCoin * price
	coin = coin - saleCoin
	# print("卖	RMB：" + '%.2f'%money + "	btc：" + '%.4f'%coin + "	价格：" + '%s'%price)
	return {'money':money, 'coin':coin}