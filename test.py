#make new payload

#Test out the algorithms for their precision and recall
#Usage:
# >>> from test import test_algorithms
# >>> test_algorithms()
# 
# (results printed to terminal)
#

from pymongo import Connection
from json import load
from collections import defaultdict

from classifier_LICA import LICA
from classifier_DFR import DFR

def check_mappings():
	"""	Moreover uses a different set of topic names than in mozcat.
		These have been mapped in moreover_to_mozcat.json
		However, mozcat_heirarchy changes fairly often so we have to check that this is still up to date
		can be checked easily with:
		python -c "from test import check_mappings;print check_mappings()"
	"""
	
	#load the files into memory
	with open('/Users/mruttley/Documents/2015-01-13 Heirarchy/mozcat/mozcat_heirarchy.json') as f: 
		# tree is currently in the format:
		# top_level: [sub_level, sub_level, ...]
		# this is hard to look up from, so we need a set of all items which is O(1)
		mozcat = set()
		for top_level, sub_levels in load(f).iteritems():
			mozcat.update([top_level])
			mozcat.update(sub_levels)
		
	with open('moreover_to_mozcat.json') as f:
		mapping = load(f)
	
	not_found = []
	for k, v in mapping.iteritems():
		if v not in mozcat:
			not_found.append(v)
	
	if not_found:
		print "Not Found: {0}".format(sorted(list(set(not_found))))
		return False
	else:
		return True

def output_stats(results):
	"""Outputs some stats from a results object in test_algorithms"""
	
	total = sum(results[results.keys()[0]].values())
	print "Total documents tested: {0}".format(total)
	
	for algorithm, tallies in results.iteritems():
		print "    Algorithm: {0}".format(algorithm.upper())
		print "      Correct: {0}".format(tallies['correct'])
		print "    Incorrect: {0}".format(tallies['incorrect'])
		print "Uncategorized: {0}".format(tallies['uncategorized'])
		print "    Precision: {0}".format(round((tallies['correct']/float(tallies['correct']+tallies['incorrect']))*100, 3) if tallies['incorrect'] > 0 else 0)
		print "       Recall: {0}".format(round((tallies['correct']+tallies['incorrect'])/float(total)*100, 3) if total > 0 else 0)
	
	print "-"*50

def test_algorithms():
	"""Tests the algorithms on Moreover data"""
	
	#set up the connection and initialize the classifiers
	db = Connection("ec2-54-87-201-148.compute-1.amazonaws.com")['moreover']['docs']
	lica = LICA()
	dfr = DFR()
	
	#load the moreover to mozcat mappings (moreover uses a different dataset)
	with open("moreover_to_mozcat.json") as mm:
		with open("/Users/mruttley/Documents/2015-01-13 Heirarchy/mozcat/mozcat_heirarchy.json") as mh:
			#bit tricky as the mapping file just gives the top/sub level, not a [top, sub] pair as needed
			#so we have to convert it
			tree = load(mh)
			
			#build a reverse tree of sub_level = [top_level, sub_level]
			#for easy lookups
			reverse_tree = {}
			for k,v in tree.iteritems():
				reverse_tree[k] = [k, "general"]
				for x in v:
					reverse_tree[x] = [k, x]
				
			#now make sure the mappings point towards those pairs rather than strings
			#the most useful format is mozcat to moreover
			mozcat_to_moreover = defaultdict(set)
			for k, v in load(mm).iteritems():
				mozcat_to_moreover[tuple(reverse_tree[v])].update([k])
	
	#something to store the results in
	results = defaultdict(lambda: {
			"correct": 0,
			"incorrect": 0,
			"uncategorized": 0
		})
	
	#iterate through the documents
	for n, document in enumerate(db.find({'topics': {'$exists':True}}, {'url':1, 'topics':1})):
		
		#classify (if they are in an object like this, they are easier to process)
		decisions = {
			'dfr': dfr.classify(document['url']),
			'lica': lica.classify(document['url'])
		}
		
		for algorithm, decision in decisions.iteritems():
			decision = tuple(decision) #have to be tuples for the mappings dictionary
			if decision[0] == 'uncategorized':
				results[algorithm]['uncategorized'] += 1
			else:
				decision = mozcat_to_moreover[decision]
				topics = set(document['topics'])
				
				if decision.intersection(topics):
					results[algorithm]['correct'] += 1
				else:
					results[algorithm]['incorrect'] += 1
		
		#output some stats occasionally
		if n % 10000 == 0:
			output_stats(results)
	
	print "Classification testing finished, final results:"
	output_stats(results)
