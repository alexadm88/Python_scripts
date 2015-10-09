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
print time_current_file
current_date_sec = time.strftime("%s")

difference = int(current_date_sec) - int(time_current_file)

""" mail """

filepath = "/usr/local/nfsen/profiles-data/live/router/otchet.txt"
basename = os.path.basename(filepath)
me = "root@flow.unilink.ru"
you = "a.katelin@unilink.ru"

html = """\
<html>
  <head></head>
  <body bgcolor="#FF6600">
    <h1 align="center" style="color:#A3FF75">Warning!!!</h1>
    <h2 style="font-style:italic; color:#8AB8E6">Сработала система определения DDOS атак.
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
print difference

if difference > 100:
    string_command_packets = ("nfdump -r %s | awk '{print $1, $4, $7, $9}'| sort -k4 -nr | head -10") % name_current_file
    string_command_flows = ("nfdump -r %s | awk '{print $1, $4, $7, $10}' | sort -k4nr| head -12 | tail -10") % new_file
    command_packets = subprocess.Popen(string_command, shell=True, stdout = subprocess.PIPE).communicate()[0].split()
    command_flows = subprocess.Popen(string_command_flows, shell=True, stdout = subprocess.PIPE).communicate()[0].split()   
    max_value_packets = command_packets[3]
    max_value_flows = command_flows[3]
    summ = 0
    for i in command_packets[7::4]:
        summ += int(i)
    avg_summ_packets = summ / int(len(command_packets[7::4]))
    for i in command_flows[7::4]:
        summ += int(i)
    avg_summ_flows = summ / int(len(command_flows[7::4]))
    command1 = str(command_packets[:4])
    command2 = str(command_flows[:4])
    command_ip = command_packets[2].split(':')[0]
    f = open('/usr/local/nfsen/profiles-data/live/router/otchet.txt' , 'w')
    f.write('Time\tProto\tIP/Port\tPackets\n\n %s \n\n Time\tProto\tIP/Port\tPackets\n\n %s' % (command1, command2))
    f.close()
    if (int(max_value_packets) / avg_summ_packets < 10) and (int(max_value_flows) / avg_summ_flows) == 1:
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
    string_command_packets = ("nfdump -r %s | awk '{print $1, $4, $7, $9}' | sort -k4nr| head -10") % new_file
    string_command_flows = ("nfdump -r %s | awk '{print $1, $4, $7, $10}' | sort -k4nr| head -12 | tail -10") % new_file 
    command_packets = subprocess.Popen(string_command_packets, shell=True, stdout = subprocess.PIPE).communicate()[0].split()
    command_flows = subprocess.Popen(string_command_flows, shell=True, stdout = subprocess.PIPE).communicate()[0].split()
    max_value_packets = command_packets[3]
    max_value_flows = command_flows[3]
    summ = 0
    for i in command_packets[7::4]:
        summ += int(i)
    avg_summ_packets = summ / int(len(command_packets[7::4]))
    summ = 0
    for i in command_flows[7::4]:
        summ += int(i)
    avg_summ_flows = summ / int(len(command_flows[7::4]))
    command1 = str(command_packets[:4])
    command2 = str(command_flows[:4])
    command_ip = command_packets[2].split(':')[0]
    f = open('/usr/local/nfsen/profiles-data/live/router/otchet.txt' , 'w')
    f.write('Time\tProto\tIP/Port\tPackets\n\n %s \n\n Time\tProto\tIP/Port\tPackets\n\n %s' % (command1, command2))
    f.close()
    if (int(max_value_packets) / avg_summ_packets < 10) and (int(max_value_flows) / avg_summ_flows == 1):
        smtp = smtplib.SMTP('localhost')
        smtp.sendmail(me, you, msg.as_string())
        smtp.close()
    study_str = ("nfdump -r %s | awk '{print $4, $5, $6, $7}' | grep %s") % (new_file, command_ip)
    study_command = subprocess.Popen(study_str, shell=True, stdout = subprocess.PIPE).communicate()[0]
    print type(study_command)
    print study_command[1]
    print study_str

