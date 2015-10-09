#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" Copyright Katelin Alexander alex27121988@mail.ru """
 
import MySQLdb
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


""" Mariadb """
db = MySQLdb.connect(host="localhost", user="zabbix", passwd="FUljYdlb_c", init_command="use zabbix")
cursor = db.cursor()
cursor.execute("select value from history_uint where itemid=23698 ORDER BY clock DESC LIMIT 7")
data = cursor.fetchall()
db.close()

""" conversion """
spisok = list(data)
summ = 0
for i in spisok[1:]:
    reg = str(re.findall(r'\d+', str(i))).strip('[]').replace("'", "")
    summ += int(reg)

""" average """
avg_summ = summ / int(len(spisok[1:]))


""" last number """
num =  str(re.findall(r'\d+', str(spisok[:1]))).strip('[]').replace("'", "")

""" comparision logic and mail """

me = "root@flow.unilink.ru"
you = "root@unilink.ru"
msg = MIMEMultipart('alternative')
msg['Subject'] = "System detect DDos"
msg['From'] = me
msg['To'] = you

html = """\
<html>
  <head></head>
  <body bgcolor="red">
    <h1 align="center" style="color:#A3FF75">Warning!!!</h1>
    <h2 style="font-style:italic; color:#8AB8E6">Сработала система определения DDOS атак.
    Текущее значение траффика больше среднего значения за час.
    Необходимо проверить zabbix
    </h2>
  </body>
</html>
"""
part = MIMEText(html, 'html', 'utf-8')
msg.attach(part)

if int(num) / avg_summ > 3:
    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()

