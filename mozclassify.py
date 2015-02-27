#!/usr/bin/env python

"""
Implements various Mozilla classifiers in Python (LICA, LWCA, LICA+DFR etc).
Usage:
> import mozclassify
> LICA = mozclassify.LICA()
> LICA.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
[u'hobbies & interests', u'coins']

"""

from json import load
from codecs import open as copen
from urlparse import urlparse
from re import findall
from collections import defaultdict
from tldextract import extract


class LICA:
	"""Object that can classify a url using LICA."""
	
	def __init__(self):
		"""Sets up the classifier"""
		
		#import the main payload with keywords for matching/blocking
		with copen("payload_lica.json", encoding='utf8') as f:
			self.payload = load(f)
		
		#Build a mapping in memory of keyword to category
		#The payload is kept in the reverse format to make it easier to edit
		self.positive_keywords = {}
		for top_level, sub_level in self.payload['positive_words'].iteritems():
			for category, keywords in sub_level.iteritems():
				for keyword in keywords:
					self.positive_keywords[keyword] = [top_level, category]
		
		#create a simple ignored words checker
		self.ignored_words = set(self.payload["ignore_words"])
	
	def classify(self, url):
		"""Returns a classification in the format [top_level, sub_level]
		This fits with the mozcat heirarchy/taxonomy: https://github.com/matthewruttley/mozcat"""
		
		#first check that its not a blacklisted domain
		tldinfo = extract(url)
		if tldinfo.domain in self.payload['ignore_domains']:
			if tldinfo.suffix in self.payload['ignore_domains'][tldinfo.domain]:
				return ['uncategorized', 'ignored', 1]
		
		#extract URL chunks
		words = set(findall("[a-z]{3,}", url)) #extract 3+ character words from the url
		
		#check that it is not a blacklisted path in a domain
		domain_name = tldinfo.domain + tldinfo.suffix
		if domain_name in self.payload["ignore_domains"]:
			for word in self.payload["ignore_domains"][domain_name]:
				if word in words:
					return ['uncategorized', 'ignored']
		
		#check that there are no ignored words
		if self.ignored_words.intersection(words):
			return ['uncategorized', 'ignored']
		
		#now classify
		#find words that we have classified in the payload
		matches = defaultdict(lambda: defaultdict(int))
		for word in words:
			if word in self.positive_keywords:
				match = self.positive_keywords[word]
				matches[match[0]][match[1]] += 1
		
		#sort by number of hits in the sub categories
		matches = sorted(matches.items(), key=lambda x: sum(matches[x[0]].values()), reverse=True)
		
		#get the top_level category
		if len(matches) == 1:
			top_level = matches[0][0]
		else:
			if sum(matches[0][1].values()) == sum(matches[1][1].values()): #special case if the top two are the same
				return ['uncategorized', 'no consensus']
			else:
				top_level = matches[0][0]
		
		#now calculate the sub-level category
		#must sort by number of hits after inverting (since multiple subcats can be provided)
		sub_level = defaultdict(list)
		for category, hits in matches[0][1].iteritems():
			sub_level[hits].append(category)
		sub_level = sorted(sub_level.items(), reverse=True)
		
		#now chain the top together
		sub_level = "/".join(sub_level[0][1])
		
		return [top_level, sub_level]









