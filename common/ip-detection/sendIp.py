import commands
import time
import sys
import urllib2
from urllib import urlencode

time_to_sleep = int(sys.argv[1])
time.sleep(time_to_sleep)

ifconfig_output = commands.getoutput('/sbin/ifconfig')

print ifconfig_output

values = {
	'action': 'updateData',
	'key': 'Raspberry Pi ifconfig output',
	'value': ifconfig_output
}
url = 'http://horatiu-misc-stuff.appspot.com/'
print 'Sending data to ' + url + ' . . .'
data = urlencode(values)
req = urllib2.Request(url, data)
urllib2.urlopen(req)
print 'Success!'
