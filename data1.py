import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email import encoders

from urllib.request import Request, urlopen

import urllib.request as urllib2

import sys

import bs4

import time

from nsetools import Nse
import mysql.connector

mydb = mysql.connector.connect(host ='160.153.129.236',user='jan_skarvidb', passwd='jan_skarvidb', database='jan_skarvidatabase')
mycursor = mydb.cursor()

# creating a Nse object
nse = Nse()
  

sql = "SELECT Symbol FROM ind_nifty50"

mycursor.execute(sql)
myresult = mycursor.fetchall()
nifty_list=[]
if(len(myresult)):
	# print(myresult)
	for x in myresult:
		# print(x[0])
		# getting quote of the sbin
		quote = nse.get_quote(x[0])
  
		# printing comapny name
		# print(quote['companyName'])
		  
		symbol_chng=float(quote['pChange'])
		# printing buy price

		# price=quote['buyPrice1']
		ind_quote=nse.get_index_quote("NIFTY 50")
		# nifty_50=round(float(ind_quote['pChange'],2)+2
		nifty_50=float(ind_quote['pChange'])
		store_nifty_50=nifty_50
		nifty_50=nifty_50+2
		nifty_50=round(nifty_50,2)
		sub_list=[]
		if(symbol_chng>=nifty_50):
			print(x[0])
			# print(symbol_chng)
			# print(nifty_50)
			sub_list.append(x[0])
			sub_list.append(str(symbol_chng))
			nifty_list.append(sub_list);
	print(nifty_list)
top_gainers = nse.get_top_gainers() 
# print(top_gainers)
top_gain=[]
for x in top_gainers:
	top_gain.append(x['symbol'])
print(" list of top gaining stocks for the last trading session")
print(top_gain)	
top_losers = nse.get_top_losers() 
top_lose=[]
for x in top_losers:
	top_lose.append(x['symbol'])
print(" list of top losing stocks for the last trading session")
print(top_lose)
#email_user = 'manisha@skarvisystems.co.uk'

email_user = 'anusha@skarvisystems.co.uk'

email_password =  'Skarvi@123'

#email_password = 'isha@nit_49'

#email_send = 'gokulalakshmiragu@gmail.com'

#email_send =sys.argv[2]

subject = 'NSE LIVE MARKET'


email_send="anusha@skarvisystems.co.uk"
email_send1="anusha@skarvisystems.co.uk"

res = [','.join(ele) for ele in nifty_list]

res = '\t'.join(res)

res=res+"\n\nlist of top gaining stocks for the last trading session\n\n"
res=res+'\n'.join(top_gain)


res=res+"\n\nlist of top losing stocks for the last trading session\n\n"
res=res+'\n'.join(top_lose)

body=res


msg = MIMEMultipart()
msg['From'] = email_user

msg['To'] = email_send

msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))


text = msg.as_string()

server = smtplib.SMTP('smtp.office365.com', 587)

server.starttls()

server.login(email_user, email_password)

server.sendmail(email_user, email_send,text)
server.sendmail(email_user, email_send1,text)
server.quit()
