# Obaid Farooqui
# 
# emailExtractor


import sys
import Queue
import re
import urllib2
from bs4 import BeautifulSoup
import requests

domain = sys.argv[1]
exploredPages = []
toExplore = Queue.Queue()

# make sure domain always starts with http://www.
if re.match('http', domain) == None:
	if re.match('www', domain) == None:
		domain = 'www.' + domain
	domain = 'http://' + domain

domainPattern = re.compile(domain)
emailPattern = re.compile('([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})')

toExplore.put(domain)

while not toExplore.empty():
	page = toExplore.get()
	exploredPages.append(page)
	 
	try: 
		pageHTML = requests.get(page, auth=('user', 'pass'))
	except:
		break
	else:
		soup = BeautifulSoup(pageHTML.text) 	

		for tag in soup.find_all("span"):
			url = domain + tag.get_text()
			if (str(url) not in exploredPages):
		    		toExplore.put(str(url))

		for link in soup.find_all('a'):
			url = link.get('href')

			if domainPattern.match(str(url)) != None: 
				# if it's a local url, just append it to the domain
				if (re.match('http', str(url)) == None) and (re.match('www', str(url)) == None):
					url = domain + str(url)
				if (str(link.get('href')) not in exploredPages):
		    			toExplore.put(url)

		#search the soup for emails and print them
		for match in emailPattern.findall(str(soup)):
			print match[0] + '@' + match[1] + '.' + match[2]






