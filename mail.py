#!/usr/bin/env python
#-*-coding: UTF-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
import os

filepath = "/usr/local/nfsen/profiles-data/live/router/backup.tar.gz"
basename = os.path.basename(filepath)
address = "a.katelin@unilink.ru"

html = """\
<html>
  <head></head>
  <body bgcolor="red">
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
msg['From'] = address
msg['To'] = address
msg.attach(part)
msg.attach(part1)

# Send mail
smtp = smtplib.SMTP('localhost')
smtp.sendmail(address, address, msg.as_string())
smtp.close()
