# -*- coding:utf-8 -*-
import time,datetime

def str_to_strptime(str):
    if str != None and str != '':
        return int(time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S")))
    else:
        return int(time.time())


def strptime_to_str(timeStamp):
    if timeStamp != None:
        return datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
