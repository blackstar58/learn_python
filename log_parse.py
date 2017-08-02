#!/usr/bin/python

import sys
import re
import time
import datetime

parts = [
    r'(?P<host>\S+)',  # host %h
    r'\S+',  # indent %l (unused)
    r'(?P<user>\S+)',  # user %u
    r'\[(?P<time>.+)\]',  # time %t
    r'"(?P<request>.+)"',  # request "%r"
    r'(?P<status>[0-9]+)',  # status %>s
    r'(?P<size>\S+)',  # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',  # referer "%{Referer}i"
    r'"(?P<agent>.*)"',  # user agent "%{User-agent}i"
]

pattern = re.compile(r'\s+'.join(parts) + r'\s*\Z')

for line in sys.stdin:
    m = pattern.match(line)
    res = m.groupdict()

    if res["user"] == "-":
        res["user"] = None

    res["status"] = int(res["status"])

    if res["size"] == "-":
        res["size"] = 0
    else:
        res["size"] = int(res["size"])

    if res["referer"] == "-":
        res["referer"] = None


    class Timezone(datetime.tzinfo):


    def __init__(self, name="+0000"):
        self.name = name
        seconds = int(name[:-2]) * 3600 + int(name[-2:]) * 60
        self.offset = datetime.timedelta(seconds=seconds)


    def utcoffset(self, dt):
        return self.offset


    def dst(self, dt):
        return timedelta(0)


    def tzname(self, dt):
        return self.name


    tt = time.strptime(res["time"][:-6], "%d/%b/%Y:%H:%M:%S")
    tt = list(tt[:6]) + [0, Timezone(res["time"][-5:])]
    res["time"] = datetime.datetime(*tt)

print"{0}".format(pattern)


