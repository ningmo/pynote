# -*- coding: utf-8 -*-
import sys
import xlrd
import logging
import glob
from yaml import load
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tornado import template
import time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',filename = 'log.txt',filemode='a')

def SendMail(to_mail, subject, message):
    """
    @param to_mail:
    @param subject:
    @param message:   
    """
    conf = load(open('config.yaml','r'))
    from_email = conf['sender']
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_mail
    msg['Subject'] = subject
    con = MIMEText(message, 'html', 'utf-8')
    msg.attach(con)
    server = smtplib.SMTP(conf['smtp'])
    rs = False
    try:
        server.login(conf['user'], conf['password'])
        server.sendmail(from_email, to_mail, msg.as_string())
        rs = True
    except Exception, what:
        logging.warning(what)
        rs = False
    finally:
        server.quit()
        return rs

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # handler = logging.handlers.RotatingFileHandler('log.txt', maxBytes = 1024*1024, backupCount = 5)
    # fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    # formatter = logging.Formatter(fmt)

    xlsLst = glob.glob('*.xls')
    tplContent = open('tpl/t.tpl','r').read().decode('utf-8')
    for i in xlsLst:
        workbook = xlrd.open_workbook(i)
        table = workbook.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        heads = []
        for r in range(nrows):
            data = []
            if r == 0:
                heads = table.row_values(r)
            else:
                data = table.row_values(r)
                t = template.Template(tplContent)
                message = t.generate(heads=heads[0:-1],data=data[0:-1])
                r = SendMail(data[-1],i[0:-4],message)
                if r:
                    logging.info(data[-1])
                    print 'send to %s' % (data[-1])
                else:
                    logging.warning(data[-1])
                    print 'failed to %s' % (data[-1])
                time.sleep(1)
