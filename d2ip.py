#!/usr/bin/python3
import sys 
import time
import queue
import socket
import threading
from colorama import Fore, Style, init
from requests.exceptions import ConnectionError


#enable coloring on win
try:
	import win_unicode_console
	win_unicode_console.enable()
	init()
except ImportError:
	pass

#queue and lock var
domains = queue.Queue()
lock = threading.Lock()

# reading args
try:
	sublist = sys.argv[1]
except IndexError:
	sublist = ""

# reading file
try:
	subfile = open(sublist, 'r')
except IOError:
	subfile = sublist.split(",")

# populate queue with domains
for sub in subfile:
	domains.put(sub.strip())

try:
	subfile.close()
except:
	pass

# checking cname
def Check(domain):
	try:
		req=socket.gethostbyname(domain)
		socket.setdefaulttimeout(1)
		res=domain + ":" + req
		with lock: print(res)
	except:
		pass
	domains.task_done()

# starting threads
while not domains.empty():
	domain = domains.get()
	try:
		threading.Thread(target=Check,args=(domain,)).start()
	# avoid thread start error
	except RuntimeError:
		domains.task_done()
		domains.put(domain)

# wait until all threads done
domains.join()