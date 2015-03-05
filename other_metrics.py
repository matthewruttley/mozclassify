#!/usr/bin/env python

#Some other metrics like IAB Illegal Content detection

def detect_content():
	"""Tries to detect the top level category of a page's content"""

def IAB_content_rating():
	"""Tries to judge the IAB content rating of a page"""
	
	ratings = {
		1: "All Audiences",
		2: "Everyone over 12",
		3: "Mature Audiences",
		4: "Unknown/Undisclosed"
	}

def IAB_non_standard_content(url='', classification=[]):
	"""Tries to detect if a page contains IAB non-standard content"""

	kws = {
		"Extreme Graphic/Explicit Violence": [],
		"Pornography": [],
		"Profane Content": [],
		"Hate Content": [],
		"Under Construction": [],
		"Incentivized": [],
		"Unmoderated UGC": []
	}
	
	if classification:
		if classification[0] == 'adult':
			return "Pornography"
	else:
		return "Not Applicable"
	
def IAB_illegal_content():
	"""Tries to detect if a page contains content that the IAB would deem illegal"""
	
	kws = {
		"Illegal Content": [],
		"Warez": [],
		"Spyware/Malware": [],
		"Copyright Infringement": [],
	}

def brand_safe():
	"""Tries to judge if a page is brand-safe"""

def malicious():
	"""Attempts to detect malicious content in a page"""

def objectionable():
	"""Tries to judge if a page is objectionable"""







