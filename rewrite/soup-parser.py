#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, re, argparse

def flags():
	parser = argparse.ArgumentParser(description='Soup Feed Parser', epilog='Bla Bla Bla')
	parser.add_argument('username', metavar='username', help='Username as Input')
	parser.add_argument('-l', type=int, dest='loops', help='How many Web pages should I crawl')
	return parser.parse_args()
        
def soupfeed():
	images = []
	rx = r'url="(http://.\.asset\.soup\.io/asset/\d{4}/.{4}_.{4})(_.*)?\.(jpeg|jpg|gif|png)'

	url='http://%s.soup.io/rss/' % flags().username    
	code = urllib.urlopen(url).read()

	for line in code.split('\n'):
		imagesearch = re.search(rx, line)
		if imagesearch:
			image = '%s.%s' % (imagesearch.group(1), imagesearch.group(3))
			images.append(image)
	
		return images

def soupweb():
	images = []
	rx = r'src="(http://.\.asset\.soup\.io/asset/\d{4}/.{4}_.{4})(_.*)?\.(jpeg|jpg|gif|png)'
	sx = r'SOUP.Endless.next_url.*/(since/\d*)'
	since = ''
	loops = 5

	if flags().loops != None:
		loops = flags().loops

		for loop in range(0, loops):
			url='http://%s.soup.io/%s' %(flags().username, since)
			code = urllib.urlopen(url).read()

			for line in code.split('\n'):
				imagesearch = re.search(rx, line)
				if imagesearch and not re.search('square', imagesearch.group(0)):
					image = '%s.%s' % (imagesearch.group(1), imagesearch.group(3))
					images.append(image)
				if re.search(sx, line):
					since = re.search(sx, line).group(1)

	return images

def main():
	images = set(soupfeed())
	images.update(soupweb())
	for i in sorted(images):
		print i

# Start
if __name__ == '__main__':
	main()