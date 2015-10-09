import urllib2
from urllib import urlencode

def updateData(key, value):
	values = {
		'action': 'updateData',
		'key': str(key),
		'value': str(value)
	}
	url = 'http://horatiu-misc-stuff.appspot.com/'
	data = urlencode(values)
	req = urllib2.Request(url, data)
	urllib2.urlopen(req)