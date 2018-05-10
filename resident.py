#!/usr/bin/env python3

try:    
    import urllib.request
    import socket
    import sys
except ImportError: # Python 2
    from urllib2 import urlopen

from bs4 import BeautifulSoup

URL_TO_PARSE = 'http://podcast.hernancattaneo.com/'

def timeout():
	timeout = 10
	socket.setdefaulttimeout(timeout)

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def get_results(page_source):
	download_links = []

	soup = BeautifulSoup(page_source, "lxml")
	results = soup.find_all("a", class_="download_link")

	# Format response in a dictonary
	for resident in results:
		download_links.append(resident.get('href'))

	# next_page = soup.find_all("a", class_="next-page")
	return download_links

def get_page(query):
	if not query:
		query = URL_TO_PARSE
	# Verificamos conexion
	try:
		# urllib will auto-detect your proxy settings and use those
		proxy_support = urllib.request.ProxyHandler({})
		opener = urllib.request.build_opener(proxy_support)
		urllib.request.install_opener(opener)
		# <Read main page>
		req = urllib.request.Request(URL_TO_PARSE)
		response = urllib.request.urlopen(req)
		page_source = response.read()	
		# Close connection
		response.close()	
	except ConnectionRefusedError:
		pass
		
	return page_source

def get_size(link):
	try:
		return int(urllib.urlopen(link).headers.get("Content-Length"))
	except:
		return 0	

def download(link, filename = ""):
	#print("File size: {} MB (0 means unknown)".format(str(get_size(link)/10.0**6)[:5]))
	if not filename:
		filename = link.split('/')[-1]
	print("Downloading...")
	try:
		urllib.request.urlretrieve(link, filename, reporthook)
		print ("Done!")
	except:
		print ("404: Couldn't download file")	

def get_link(page_source, n):
    # "n" is the position in the list in the results    
    print(page_source)
    return page_source[n]

def download_using_wget(link): # Use instead if you have wget
	from os import system
	system('wget -c "{}"'.format(link))

def main():
	print ("MP3 Resident downloader")
	query = input("URL <empty by default>: ")
	page = get_page(query)
	n = 1
	results = get_results(page)

	for title in results:
		print ("{}.{}".format(n, title))
		n += 1

	n = int(input("Cual bajamos ? "))
	download(get_link(results, n)) # You can replace by download_with_wget()

 # Code to run when this is the main program here
if __name__ == '__main__':
	# Code to run when this is the main program here
	main()
