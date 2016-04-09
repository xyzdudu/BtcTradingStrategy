# -*- coding: utf-8 -*-
#���ڷ���OKCOIN �ֻ�REST API
from HttpMD5Util import buildMySign,httpGet,httpPost

class BtcSpot(object):
	def __init__(self, url,apikey,secretkey):
		self.__url = url
		self.__apikey = apikey
		self.__secretkey = secretkey

	#��ȡOKCOIN�ֻ�������Ϣ
	def ticker(self,symbol = ''):
		TICKER_RESOURCE = "/api/v1/ticker.do"
		params=''
		if symbol:
			params = 'symbol=%(symbol)s' %{'symbol':symbol}
		return httpGet(self.__url,TICKER_RESOURCE,params)

	#��ȡOKCOIN�ֻ��г������Ϣ
	def depth(self,symbol = ''):
		DEPTH_RESOURCE = "/api/v1/depth.do"
		params=''
		if symbol:
			params = 'symbol=%(symbol)s' %{'symbol':symbol}
		return httpGet(self.__url,DEPTH_RESOURCE,params)

	#��ȡOKCOIN�ֻ���ʷ������Ϣ
	def trades(self,symbol = ''):
		TRADES_RESOURCE = "/api/v1/trades.do"
		params=''
		if symbol:
			params = 'symbol=%(symbol)s' %{'symbol':symbol}
		return httpGet(self.__url,TRADES_RESOURCE,params)

	#��ȡ���رһ����رҵ�K������
	def kline(self,symbol = '',timetype = '',size = '',since = ''):
		KLINE_RESOURCE = "/api/v1/kline.do"
		params=''
		if symbol:
			params = 'symbol=%(symbol)s' %{'symbol':symbol}
		if timetype:
			params += '&type=%(timetype)s' %{'timetype':timetype}
		if size:
			params += '&size=%(size)s' %{'size':size}
		if since:
			params += '&since=%(since)s' %{'since':since}
		return httpGet(self.__url,KLINE_RESOURCE,params)

	#��ȡ�û��ֻ��˻���Ϣ
	def userinfo(self):
		USERINFO_RESOURCE = "/api/v1/userinfo.do"
		params ={}
		params['api_key'] = self.__apikey
		params['sign'] = buildMySign(params,self.__secretkey)
		return httpPost(self.__url,USERINFO_RESOURCE,params)

	#�ֻ�����
	def trade(self,symbol,tradeType,price='',amount=''):
		TRADE_RESOURCE = "/api/v1/trade.do"
		params = {
			'api_key':self.__apikey,
			'symbol':symbol,
			'type':tradeType
		}
		if price:
			params['price'] = price
		if amount:
			params['amount'] = amount

		params['sign'] = buildMySign(params,self.__secretkey)
		return httpPost(self.__url,TRADE_RESOURCE,params)

	#�ֻ������µ�
	def batchTrade(self,symbol,tradeType,orders_data):
		BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
		params = {
			'api_key':self.__apikey,
			'symbol':symbol,
			'type':tradeType,
			'orders_data':orders_data
		}
		params['sign'] = buildMySign(params,self.__secretkey)
		return httpPost(self.__url,BATCH_TRADE_RESOURCE,params)

	#�ֻ�ȡ������
	def cancelOrder(self,symbol,orderId):
		CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
		params = {
			'api_key':self.__apikey,
			'symbol':symbol,
			'order_id':orderId
		}
		params['sign'] = buildMySign(params,self.__secretkey)
		return httpPost(self.__url,CANCEL_ORDER_RESOURCE,params)

	#�ֻ�������Ϣ��ѯ
	def orderinfo(self,symbol,orderId):
		ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
		params = {
			'api_key':self.__apikey,
			'symbol':symbol,
			'order_id':orderId
		}
		params['sign'] = buildMySign(params,self.__secretkey)
		return httpPost(self.__url,ORDER_INFO_RESOURCE,params)

	#�ֻ�����������Ϣ��ѯ
	def ordersinfo(self,symbol,orderId,tradeType):
		ORDERS_INFO_RESOURCE = "/api/v1/orders_info.do"
		params = {
			'api_key':self.__apikey,
			'symbol':symbol,
			'order_id':orderId,
			'type':tradeType
		}
		params['sign'] = buildMySign(params,self.__secretkey)
		return httpPost(self.__url,ORDERS_INFO_RESOURCE,params)

	#�ֻ������ʷ������Ϣ
	def orderHistory(self,symbol,status,currentPage,pageLength):
		ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
		params = {
			'api_key':self.__apikey,
			'symbol':symbol,
			'status':status,
			'current_page':currentPage,
			'page_length':pageLength
		}
		params['sign'] = buildMySign(params,self.__secretkey)
		return httpPost(self.__url,ORDER_HISTORY_RESOURCE,params)