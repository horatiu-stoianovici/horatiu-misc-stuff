#!/usr/bin/python

from datetime import timedelta

def getUptimeString():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(timedelta(seconds = uptime_seconds))

    return uptime_string