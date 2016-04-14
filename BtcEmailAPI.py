from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
	
from_addr = '*@163.com'
password = '*'
to_addr = '*@qq.com'
smtp_server = 'smtp.163.com'		

def sendMail(to_list,sub,connect):
	print(to_list + '%s'%sub + '%s'%connect)
	me = 'hello' + '<' + from_addr + '>'
	msg = MIMEText(connect,'plain','utf-8')
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = to_list
	try:
		server = smtplib.SMTP()
		server.connect(smtp_server)
		server.login(from_addr,password)
		server.sendmail(me,to_list,msg.as_string())
		server.close()
		return True
	except ZeroDivisionError as e:
		print(e)
		return False