#!/usr/bin/env python

from flask import Flask, render_template, request
from classifier_LICA import LICA
from other_metrics import IAB_non_standard_content

#set up the server
app = Flask(__name__)
#set up LICA
classifier = LICA()


@app.route('/', methods=['GET'])
def show_classifier_page():
	
	data = None
	if 'url' in request.args:
		data = {}
		url = request.args.get('url')
		classification = classifier.classify(url)
		data['mozcat_tier_1'] = classification[0]
		data['mozcat_tier_2'] = classification[1]
		data['url'] = url
		data['iab_non_standard_content'] = IAB_non_standard_content(url, classification)
	
	return render_template("index.html", data=data)

if __name__ == '__main__':
	app.debug = True
	app.run()