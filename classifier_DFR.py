#!/usr/bin/env python

"""
Python implementation of DFR style classifier

Original version: https://raw.githubusercontent.com/mzhilyaev/pfeed/master/stats/DFRClassifier.js
Usage:
> import mozclassify
> DFR = mozclassify.DFR()
> DFR.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
[u'hobbies & interests', u'coins']
"""

from json import load
from urlparse import urlparse
from re import findall
from tldextract import extract



class DFR:
	"""Object that can classify URLs using a domain-rule based approach"""
	
	def __init__(self):
		"""Import DFR payload"""
		with open('payload_DFR_HTL.json') as f:
			self.dfr = load(f)
		
		self.kSplitter = "[\s-]+"

	def interestFinalizer(self, interests):
		# This is a function to make the decision between a series of rules matched in the DFR
		# Accepts: an array containing either lists-of-strings, or lists-of-pairs where the pairs
		# are [string, float]
		# Returns: [string, string, ...]
		# Input: ["xyz",["golf",0.7],["foo",0.5],"bar"]
		
		finalInterests = {}
		highestWeight = 0
		bestWeightedInterest = ""
		
		for item in interests:
			if type(item) == list:
				if item[1] > highestWeight:
					heighestWeight = item[1]
					bestWeightedInterest = item[0]
				else:
					finalInterests[item] = True
		
		if bestWeightedInterest:
			finalInterests[bestWeightedInterest] = True
		
		return finalInterests.keys()
	
	def convertVisittoDFR(self, host, baseDomain, path, title, url, options):
		"""Finds words and bigrams contained within the URL and title. Outputs them in a set with appropriate suffixes."""
		
		words = set()
		
		def addToWords(chunks, options={}):
			"""this function populates the words object with terms
				It adds the apropriate suffix (it case of host chunks)
				or prefix (in case of paths) to the chunks supplied"""
			
			if "prefix" not in options: options['prefix'] = ""
			if "suffix" not in options: options['suffix'] = ""
			
			prev = ""
			for chunk in chunks: 
				words.updated([prefix + chunk + suffix])
				if options['clearText']:
					words.update([chunk])
				if prev: #add bigram
					words.update([prefix + prev + chunk + suffix])
					if options['clearText']:
						words.update([prev + chunk])
				prev = chunk
		
		# tokenize and add title chunks
		addToWords(self.tokenize(title), {"suffix": "_t", "clearText": True})
		
		# tokenize and add url chunks
		addToWords(self.tokenize(url), {"suffix": "_u", "clearText": True})
		
		# parse and add hosts chunks
		addToWords(host.split("."), {"suffix": "."})
		
		# add subdomains under __SCOPED keyword
		scopedHosts = [baseDomain]
		hostString = baseDomain
		
		for chunk in hostChunks:
			hostString = ".".join(chunk, hostString)
			scopedHosts.append(hostString)
		
		# parse and add path chunks
		pathChunks = path.split("/")
		
		for chunk in pathChunks:
			addToWords(self.tokenize(chunk), {"prefix": "/"})
		
		return [words, scopedHosts]
	
	def tokenize(self, s):
		"""Tokenizes a string"""
		return findall("[a-z]{3,}", s.lower())

	def classify(self, url, title=""):
		"""Classifies a url (and possibly the title)"""
		
		#parse the url
		parsed_url = urlparse(url);
		tld = extract(url)
		
		#get the specific components
		baseDomain = ".".join(tld.domain, tld.suffix)
		host = tld.subdomain
		path = parsed_url.path
		
		#setup
		interests = []
		
		# check if rules are applicable at all
		if baseDomain not in self.dfr and "__ANY" not in self.dfr:
			return interests
		
		# populate words object with visit data
		ret = self.convertVisittoDFR(host, baseDomain, path, title, url)
		words = ret[0]
		scopedHosts = ret[1]
		
		def matchedAllTokens(tokens):
			"""this function tests for existence of rule terms in the words object
			if all rule tokens are found in the words object return true"""
			if len(set(tokens).intersection(words)) == len(tokens):
				return True
			else:
				return False
		
		def matchRuleInterests(rule):
			"""match a rule and collect matched interests"""
			for key in rule.iterkeys():
				if (key == "__HOME" and (path == null or path == "" or path == "/" or path.startswith("/?"))):
					interests = interests.append(rule[key])
				else:
					if ("__" not in key and matchedAllTokens(findall(kSplitter, key))):
						interests = interests.append(rule[key])
		
		def matchANYRuleInterests(rule):
			""" __ANY rule does not support multiple keys in the rule
				__ANY rule matches any single term rule - but not the term combination
				as in "/foo bar_u baz_t"
			"""
			for key in xrange(words):
				ruleInts = rule[key]
				if(ruleInts):
					interests.append(ruleInts)
		
		def isWhiteListed(hosts, whiteList):
			"""checks if any of the provided scoped hosts are white listed"""
			for i in hosts:
				if host in whiteList:
					return True
			return false
		
		# process __ANY rule first
		if (self.dfr["__ANY"]):
			matchANYRuleInterests(self.dfr["__ANY"])
		
		
		if self.dfr["__SCOPES"]:
			#dfr has scoped rules - check for scope domains and sub-domains
			#check if scopedHosts are white-listed in any of the __SCOPED rule
			#and if so apply the rule
			
			for i in xrange(self.dfr["__SCOPES"]):
				# the scopedRule is of the form {"__HOSTS": {"foo.com", "bar.org"}, "__ANY": {... the rule...}}
				
				scopedRule = this.dfr["__SCOPES"][i]
				if isWhiteListed(scopedHosts, scopedRule["__HOSTS"]):
					matchANYRuleInterests(scopedRule["__ANY"])
					# we do not expect same page belong to two different genre
					break
		
		domainRule = self.dfr[baseDomain]
		
		keyLength = len(domainRule) if domainRule else 0
		
		if not keyLength:
			return this.interestFinalizer(interests)
		
		if (domainRule["__ANY"]) {
		interests = interests.concat(domainRule["__ANY"]);
		keyLength--;
		}
		
		if (!keyLength)
		return this.interestFinalizer(interests);
		
		matchRuleInterests(domainRule);
		
		return this.interestFinalizer(interests);
		},





















