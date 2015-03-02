#!/usr/bin/env python

"""
Python implementation of Latent IAB Category Allocation (LICA)
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

def make_tree(levels, end):
	"""Recursively builds a tree.
	`levels` are levels you want to integrate, e.g. ['one', 'two', 'three']
	`end` is the value of the end item e.g. 'test'
	The result would be: {'one': {'two': {'three': 'test'}}}
	"""
	if len(levels) == 1:
		return {levels[0]: end}
	else:
		return {levels[0]: make_tree(levels[1:], end)}

def check_tree(levels, tree):
	"""Recursively checks a tree similar to the one made above in make_tree()"""
	if len(levels) == 1:
		if levels[0] in tree:
			if type(tree[levels[0]]) != dict:
				return tree[levels[0]]
		return False
	else:
		if levels[0] in tree:
			return check_tree(levels[1:], tree[levels[0]])
		else:
			return False

def merge(a, b, path=None):
    "merges b into a: http://stackoverflow.com/a/7205107/849354"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

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
		
		#import the domain rules
		with copen("payload_domain_rules.json", encoding='utf8') as f:
			self.rules = load(f)
		
		#convert the host rules into an easily searchable format
		# e.g. 		"au.movies.yahoo.com": "television",
		# 			should be: "yahoo.com": { 'movies': { 'au': ['arts & entertainment', 'television'] } }
		
		self.host_rules = defaultdict(dict)
		for host_rule, category in self.rules['host_rules'].iteritems():
			domain = extract(host_rule) 				#ExtractResult(subdomain='au.movies', domain='yahoo', suffix='com')
			tld = domain.domain + "." + domain.suffix 	# yahoo.com
			host = domain.subdomain.split('.') 			#['au', 'movies']
			tree = make_tree(host[::-1], category) 	#{ 'movies': { 'au': ['arts & entertainment', 'television'] } }
			merge(self.host_rules, {tld: tree})	#merge the host rules with this new data
		
		#convert the path rules into an easily searchable format
		self.path_rules = defaultdict(dict)
		for path_rule, category in self.rules['path_rules'].iteritems():
			domain = extract(path_rule) 
			tld = domain.domain + "." + domain.suffix 	#sort of ignoring host+path rules, those can be covered by full DFR later
			path = path_rule.split('/')[1]
			self.path_rules[tld][path] = category
	
	def classify(self, url):
		"""Returns a classification in the format [top_level, sub_level]
		This fits with the mozcat heirarchy/taxonomy: https://github.com/matthewruttley/mozcat"""
		
		#first check that its not a blacklisted domain
		tldinfo = extract(url)
		if tldinfo.domain in self.payload['ignore_domains']:
			if tldinfo.suffix in self.payload['ignore_domains'][tldinfo.domain]:
				return ['uncategorized', 'ignored', 1]
		
		#check if it is a single topic site
		tld = tldinfo.domain + tldinfo.suffix
		if tld in self.rules['domain_rules']:
			return ['uncategorized', 'ignored', 1]
		
		#check if it is a single topic host
		if tldinfo.subdomain:
			if tld in self.host_rules:
				domain_tree = self.host_rules[tld]
				match = check_tree(tldinfo.subdomain.split('.'), domain_tree)
				if match:
					return match
		
		#check if it is a single topic path
		if tld in self.path_rules:
			path = url.split('/')
			if len(path) > 1:
				path = path[1]
				if path in self.path_rules[tld]:
					return self.path_rules[tld][path]
		
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
