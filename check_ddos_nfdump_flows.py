#!/usr/bin/env python
#-*-coding: UTF-8 -*-

""" Copyright Katelin Alexandr <alex27121988@mail.ru>
         
Detect ddos base nfdump """

import os
from subprocess import PIPE, Popen
import subprocess
import smtplib
import datetime
import time
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.Encoders import encode_base64
from email import Encoders

""" path selection algorithm """

path = ('/usr/local/nfsen/profiles-data/live/router/')
os.chdir(path)

name_current_file = subprocess.Popen('ls | grep nfcapd.current', shell=True, stdout = subprocess.PIPE).communicate()[0].strip()
time_current_file = int(os.path.getctime(name_current_file))

current_date_sec = time.strftime("%s")

difference = int(current_date_sec) - int(time_current_file)

""" mail """

filepath = "/usr/local/nfsen/profiles-data/live/router/otchet1.txt"
basename = os.path.basename(filepath)
me = "root@flow.unilink.ru"
you = "a.katelin@unilink.ru"

html = """\
<html>
  <head></head>
  <body bgcolor="#009933">
    <h1 align="center" style="color:#CC3300">Warning!!!</h1>
    <h2 style="font-style:italic; color:#99FF66">Сработала система определения DDOS атак.
    Текущее значение траффика больше среднего значения на порядок. 
    </h2>
  </body>
</html>
"""
part1 = MIMEText(html, 'html', 'utf-8')


# Compose attachment
part = MIMEBase('application', "octet-stream")
part.set_payload(open(filepath,"rb").read() )
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)

# Compose message
msg = MIMEMultipart()
msg['Subject'] = "System detect DDos base on nfdump"
msg['From'] = me
msg['To'] = you
msg.attach(part)
msg.attach(part1)
""" nfdump check packets """

if difference > 100:
    string_command = ("nfdump -r %s | awk '{print $1, $4, $7, $10}'| sort -k4 -nr | head -12 | tail -10") % name_current_file
    command = subprocess.Popen(string_command, shell=True, stdout = subprocess.PIPE).communicate()[0].split()
    max_value = command[3]
    print max_value
    summ = 0
    for i in command[7::4]:
        summ += int(i)
    avg_summ = summ / int(len(command[7::4]))
    command1 = str(command[:4])
    f = open('/usr/local/nfsen/profiles-data/live/router/otchet1.txt' , 'w')
    f.write('Time\tProto\tIP/Port\tFlows\n\n %s' % command1)
    f.close()
    if int(max_value) / avg_summ == 1:
        smtp = smtplib.SMTP('localhost')
        smtp.sendmail(me, you, msg.as_string())
        smtp.close()
else:
    now_date = datetime.date.today()
    now_year = now_date.year
    now_month = time.strftime("%m")
    now_day = time.strftime("%d")
    path = ('/usr/local/nfsen/profiles-data/live/router/%s' + '/' + '%s' + '/' + '%s') % (now_year, now_month, now_day)
    os.chdir(path)
    new_file = subprocess.Popen('ls -t | head -1', shell=True, stdout = subprocess.PIPE).communicate()[0].strip()
    string_command = ("nfdump -r %s | awk '{print $1, $4, $7, $10}' | sort -k4nr| head -12 | tail -10") % new_file
    command = subprocess.Popen(string_command, shell=True, stdout = subprocess.PIPE).communicate()[0].split()
    print command
    max_value = command[3]
    print max_value
    print command[7::4]
    summ = 0
    for i in command[7::4]:
        summ += int(i)
    avg_summ = summ / int(len(command[7::4]))
    command1 = str(command[:4])
    f = open('/usr/local/nfsen/profiles-data/live/router/otchet1.txt' , 'w')
    f.write('Time\tProto\tIP/Port\tFlows\n\n %s' % command1)
    f.close()
    if int(max_value) / avg_summ == 1:
        smtp = smtplib.SMTP('localhost')
        smtp.sendmail(me, you, msg.as_string())
        smtp.close()

