#!/usr/bin/python
import datetime
import json
import sys
import os
import urllib
import urllib2
from optparse import OptionParser
import pprint

'''
Project     :       Apache Solr 4.x Health Check
Version     :       0.1
Author      :       Douglas Land <dsl@looprock.com>
Summary     :       This program is a nagios plugin that checks Apache 4.0 Solr Health
Dependency  :       Linux/nagios/Python-2.6

Usage :
```````
shell> python check_solr.py
'''
pp = pprint.PrettyPrinter(indent=4)

#--------------------------|
# Main Program Starts Here |
#--------------------------|
# Command Line Arguments Parser
cmd_parser = OptionParser(version = "%prog 0.1")
cmd_parser.add_option("-a", "--allcores", action = "store_true", dest = "allcores", help = "Execute check against all cores [only valid for type 'status, path relative to status/<core>']")
cmd_parser.add_option("-d", "--debug", action = "store_true", dest = "bug", help = "Enable debug mode")
cmd_parser.add_option("-D", "--datecompare", action = "store_true", dest = "datecompare", help = "Do a date comparison, seconds from current time")
cmd_parser.add_option("-H", "--host", type = "string", action = "store", dest = "solr_server", help = "SOLR Server IPADDRESS")
cmd_parser.add_option("-p", "--port", type = "string", action = "store", dest = "solr_server_port", help = "SOLR Server port", default = 8983)
cmd_parser.add_option("-t", "--type", type = "string", action = "store", dest = "status_type", help = "Which admin interface to hit: status, ping, stats", default = "ping")
cmd_parser.add_option("-e", "--eval", type = "string", action = "store", dest = "eval_type", help = "Type of evaluation: gt, lt, eq, ne, le, ge, is, not", default = "eq")
cmd_parser.add_option("-P", "--path", type = "string", action = "store", dest = "path", help = "Path inside the json object you want to check, / delimited, RE: responseHeader/status", default = "responseHeader/status")
cmd_parser.add_option("-w", "--warning", type = "string", action = "store", dest = "warning", help = "Exit with WARNING status if criteria met", metavar = "Warning")
cmd_parser.add_option("-c", "--critical", type = "string", action = "store", dest = "critical", help = "Exit with ERROR status if criteria met", metavar = "Critical")
(cmd_options, cmd_args) = cmd_parser.parse_args()

# Check the Command syntax
if not (cmd_options.solr_server and cmd_options.solr_server_port and cmd_options.status_type and cmd_options.eval_type and cmd_options.path):
	cmd_parser.print_help()
	sys.exit(3)

# make sure we have something to check
if not (cmd_options.critical or cmd_options.warning):
	print "ERROR: you need to critical, warning, or both"
	cmd_parser.print_help()
	sys.exit(1)

# make sure we didn't get a bad eval type
if cmd_options.eval_type not in ["gt", "lt", "eq", "le", "ge", "is", "not", "ne"]:
	print "ERROR: invalid eval type %s!" % cmd_options.eval_type
	cmd_parser.print_help()
        sys.exit(1)

# debug stuff
if cmd_options.bug:
	print "DEBUG: "
        print cmd_options
        print "cmd_options.warning: %s" % cmd_options.warning
        print "cmd_options.critical: %s" % cmd_options.critical
        print "cmd_options.solr_server: %s" % cmd_options.solr_server
        print "cmd_options.solr_server_port: %s" % cmd_options.solr_server_port
        print "cmd_options.status_type: %s" % cmd_options.status_type
        print "cmd_options.eval_type: %s" % cmd_options.eval_type
        print "cmd_options.path: %s" % cmd_options.path
        print "cmd_options.allcores: %s" % cmd_options.allcores

# read solr admin data
def getsolrsgtatus(server,port,type="status"):
	if type == "status":
		path = "cores?action=STATUS&wt=json&memory=true"
	elif type == "ping":
		# http://etl15.vast.com:9000/solr/admin/ping?wt=json
		path = "ping?wt=json"
	elif type == "stats":
		# http://etl15.vast.com:9000/solr/admin/plugins?stats=true&wt=json
		path = "plugins?stats=true&wt=json"
        url = "http://%s:%s/solr/admin/%s" % (server,port,path)
	if cmd_options.bug:
		print "DEBUG: %s" % url
	try:
        	conn = urllib2.urlopen(url)
	except urllib2.URLError, e:
		print "ERROR: %s" % (e)
		sys.exit(returnlevel("ERROR"))
        f = json.load(conn)
	return f

# return errors based on: http://nagios.sourceforge.net/docs/3_0/pluginapi.html
def returnlevel(level):
	if level == "WARNING":
		y = 1
	elif level == "ERROR":
		y = 2
	else:
		y = 3
	return y

# test data returned by admin interface
def readdata(data, eval_type, level, test, path):
	m = "OK"
	y = 0
	if cmd_options.bug:
		print "DEBUG: got args: data = %s, eval_type = %s, level = %s, test = %s, path = %s" % (data, eval_type, level, str(test), path)
	q = "data"
	for i in path.split("/"):
		if i:
			q += "['%s']" % i
	x = eval(q)
	if cmd_options.datecompare:
		now = datetime.datetime.now()
		v = datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")
		tmp = now - v
		x = tmp.total_seconds()
	if cmd_options.bug:
		print "DEBUG: testing %s %s %s" % (str(x), eval_type, str(test))
	if eval_type == "gt":
		if float(x) > float(test):
			m = "%s: %s greater than %s" % (level, path, str(test))
			y = returnlevel(level)
	elif eval_type == "lt":
		if float(x) < float(test):
			m = "%s: %s less than %s" % (level, path, str(test))
			y = returnlevel(level)
	elif eval_type == "eq":
		if float(x) == float(test):
			m = "%s: %s equals %s" % (level, path, str(test))
			y = returnlevel(level)
	elif eval_type == "ne":
		if float(x) != float(test):
			m = "%s: %s doesn't equal %s" % (level, path, str(test))
			y = returnlevel(level)
	elif eval_type == "le":
		if float(x) <= float(test):
			m = "%s: %s less than or equal to %s" % (level, path, str(test))
			y = returnlevel(level)
	elif eval_type == "ge":
		if float(x) >= float(test):
			m = "%s: %s greater than or equal to %s" % (level, path, str(test))
			y = returnlevel(level)
	elif eval_type == "is":
		if str(x) == str(test):
			m = "%s: %s matches %s" % (level, path, str(test))
			y = returnlevel(level)
	elif eval_type == "not":
		if str(x) != str(test):
			m = "%s: %s doesn't match %s" % (level, path, str(test))
			y = returnlevel(level)
	return {"message": m, "result": y}

def testresults(data, eval_type, warning, critical, path):
	printc = "false"
	printw = "false"
	response = 0
	if warning:
		if cmd_options.bug:
			print "DEBUG: testing: readdata(%s, %s, %s, %s, %s)" % (data, eval_type, "WARNING", warning, path)
			print readdata(data, eval_type, "WARNING", warning, path)
		w = readdata(data, eval_type, "WARNING", warning, path)
		if cmd_options.bug:
			print "**** DEBUG: found w!"
			print w
		if w["result"] > response:
			printw = "true"
			response = w["result"]

	if critical:
        	if cmd_options.bug:
                	print "DEBUG: testing: readdata(%s, %s, %s, %s, %s)" % (data, eval_type, "ERROR", critical, path)
                	print readdata(data, eval_type, "ERROR", critical, path)
        	c = readdata(data, eval_type, "ERROR", critical, path)
		if cmd_options.bug:
			print "**** DEBUG: found c!"
			print c
        	if c["result"] > response:
			printc = "true"
                	response = c["result"]
	if printc == "true":
		msg = c["message"]
	else:
		if printw == "true":
			msg = w["message"]
		else:
			msg = "OK"
	return {"message": msg, "result": int(response)}

x = getsolrsgtatus(server=cmd_options.solr_server,port=cmd_options.solr_server_port,type=cmd_options.status_type)
#pp.pprint(x)

if cmd_options.allcores:
	if cmd_options.status_type != "status":
		print "ERROR: can't use allcores with anything but 'status' type!"
		sys.exit(2)
	else:
		msg = ""
		r = 0
		for i in sorted(x['status'].keys()):
			#print i
			p = "status/%s/%s" % (i, cmd_options.path)
			if cmd_options.bug:
				print "Now testing path: %s" % p
			n = testresults(x, cmd_options.eval_type, cmd_options.warning, cmd_options.critical, p)
			if n['result'] > r:
				r = n['result']
				msg += "%s, " % n['message']	
				if cmd_options.bug:
					print "**** DEBUG: return code now: %s" % str(r)
					print "**** DEBUG: msg: %s" % msg
			if cmd_options.bug:
				print "**** DEBUG: result: %s, path: %s" % (str(n), p)
		if cmd_options.bug:
			print "**** DEBUG: msg: %s" % msg
			print "**** DEBUG: return code: %s" % str(r)
		if msg:
			print msg[:-2]
		else:
			print "OK"
		sys.exit(r)
else:
	result = testresults(x, cmd_options.eval_type, cmd_options.warning, cmd_options.critical, cmd_options.path)
	print result["message"]
	sys.exit(result['result'])
