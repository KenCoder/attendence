import httplib, urllib
import csv
import json

prefix = "/administrator/components/com_civicrm/civicrm/extern/rest.php?json=1&sequential=1&debug=1&key=3297a7f5a0b36afa8f8dea3dfe1f72c1&api_key=71ab2a73ab9e146fe83e990cb4dcce6f&"

def civicrm(action):
	conn = httplib.HTTPConnection("ugno.org")
	
	conn.request("GET", prefix + urllib.urlencode(action))
	resp = conn.getresponse()
	if resp.status != 200:
		print "Failure"
		print resp.status, resp.reason
		print 'Res:' + resp.read()
		raise "Failed"
	return resp.read()
